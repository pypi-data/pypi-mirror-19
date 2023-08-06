# Copyright (C) 2017 Pier Carlo Chiodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from .base import ConfigParserBase
from .validators import *
from ..errors import ConfigError, ARouteServerError


class ConfigParserGeneral(ConfigParserBase):

    ROOT = "cfg"

    def parse(self):
        """
        Contents of cfg dict is updated/normalized by validators.
        """

        errors = False

        schema = {
            "cfg": {
                "rs_as": ValidatorASN(),
                "router_id": ValidatorIPv4Addr(mandatory=True),
                "prepend_rs_as": ValidatorBool(default=False),                      # Done
                "path_hiding": ValidatorBool(default=True),                         # Done, not tested
                "passive": ValidatorBool(default=True),                             # Done
                "gtsm": ValidatorBool(default=False),
                "add_path": ValidatorBool(default=False),                           # Done
                "filtering": {
                    "next_hop_policy": ValidatorOption("next_hop_policy",
                                                       ("strict", "same-as"),
                                                       default="strict"),           # Done
                    "ipv4_pref_len": ValidatorIPMinMaxLen(4,
                                                          default={"min": 8,
                                                                   "max": 24}),     # Done
                    "ipv6_pref_len": ValidatorIPMinMaxLen(6,
                                                          default={"min": 12,
                                                                   "max": 48}),     # Done, not tested
                    "global_black_list_pref": ValidatorListOf(
                        ValidatorPrefixListEntry, mandatory=False,
                    ),                                                              # Done
                    "max_as_path_len": ValidatorMaxASPathLen(default=32),           # Done
                    "reject_invalid_as_in_as_path": ValidatorBool(default=True),    # Done
                    "rpsl": {
                        "enforce_origin_in_as_set": ValidatorBool(default=True),    # Done
                        "enforce_prefix_in_as_set": ValidatorBool(default=True),    # Done
                        "tag_as_set": ValidatorBool(default=True)                   # Done
                    },
                    "rpki": {
                        "enabled": ValidatorBool(default=False),                    # MISSING
                        "data_source": ValidatorOption("data_source",
                                                       ("rtrsub", "rtrlib"),
                                                       mandatory=False),            # MISSING
                        "reject_invalid": ValidatorBool(mandatory=False),           # MISSING
                    },
                    "max_prefix": {                                                 # MISSING
                        "peering_db": ValidatorBool(default=True),
                        "general_limit_ipv4": ValidatorUInt(default=170000),
                        "general_limit_ipv6": ValidatorUInt(default=12000),
                        "action": ValidatorOption(
                            "action",
                            ("shutdown", "restart", "block", "warning"),
                            mandatory=False,
                            default="shutdown"
                        )
                    },
                },
                "blackhole_filtering": {                                        # Done
                    "announce_to_client": ValidatorBool(                        # Done
                        mandatory=True, default=True
                    ),
                    "policy_ipv4": ValidatorOption(                             # Done
                        "policy_ipv4",
                        ("propagate-unchanged", "rewrite-next-hop"),
                        mandatory=False),
                    "policy_ipv6": ValidatorOption(                             # Done, not tested
                        "policy_ipv6",
                        ("propagate-unchanged", "rewrite-next-hop"),
                        mandatory=False),
                    "rewrite_next_hop_ipv4": ValidatorIPv4Addr(mandatory=False),# Done
                    "rewrite_next_hop_ipv6": ValidatorIPv6Addr(mandatory=False),# Done, not tested
                },
                "control_communities": ValidatorBool(default=True),                 # Done
                "communities": {
                }
            }
        }

        if "rs_as" in self.cfg["cfg"]:
            rs_as_macro = self.cfg["cfg"]["rs_as"]
        else:
            rs_as_macro = None

        # Add communities with no fixed values to the schema.
        for comm in ["origin_present_in_as_set", "origin_not_present_in_as_set",
                     "prefix_present_in_as_set", "prefix_not_present_in_as_set",
                     "roa_valid", "roa_invalid", "roa_unknown",
                     "blackholing",
                     "do_not_announce_to_any",
                     "prepend_once_to_any", "prepend_twice_to_any",
                     "prepend_thrice_to_any"]:


            schema["cfg"]["communities"][comm] = {
                "std": ValidatorCommunityStd(rs_as_macro, mandatory=False),
                "lrg": ValidatorCommunityLrg(rs_as_macro, mandatory=False),
                "ext": ValidatorCommunityExt(rs_as_macro, mandatory=False),
            }

        # Add communities with fixed values to the schema.
        for comm, fixed_values in [
            ("do_not_announce_to_peer",
                ("0:peer_as",
                 "rs_as:0:peer_as",
                 ["rt:0:peer_as", "ro:0:peer_as"])
            ),
            ("announce_to_peer",
                ("rs_as:peer_as",
                 "rs_as:rs_as:peer_as",
                 ["rt:rs_as:peer_as", "ro:rs_as:peer_as"])
            )]:
            schema["cfg"]["communities"][comm] = {
                "std": ValidatorCommunityStd(rs_as_macro, mandatory=False,
                                            fixed_values=fixed_values[0],
                                            allow_peer_as_macro=True),
                "lrg": ValidatorCommunityLrg(rs_as_macro, mandatory=False,
                                            fixed_values=fixed_values[1],
                                            allow_peer_as_macro=True),
                "ext": ValidatorCommunityExt(rs_as_macro, mandatory=False,
                                            fixed_values=fixed_values[2],
                                            allow_peer_as_macro=True)
            }

        try:
            ConfigParserBase.validate(schema, self.cfg)
        except ARouteServerError as e:
            errors = True
            if str(e):
                logging.error(str(e))

        # If blackhole filtering policy = "rewrite-next-hop", then
        # blackhole next-hops must be provided.
        for ip_ver in (4, 6):
            bh = self.cfg["cfg"]["blackhole_filtering"]
            if not bh:
                continue
            policy = bh["policy_ipv{}".format(ip_ver)]
            if policy == "rewrite-next-hop":
                if not bh["rewrite_next_hop_ipv{}".format(ip_ver)]:
                    errors = True
                    logging.error(
                        "Since blackhole_filtering.policy_ipv{v} is "
                        "'rewrite_next_hop', an IPv{v} address must "
                        "be provided in "
                        "'rewrite_next_hop_ipv{v}'.".format(
                            v=ip_ver
                        )
                    )

        # Duplicate communities?
        communities = self.cfg["cfg"]["communities"]
        unique_communities = []
        for comm_tag in communities:
            comm = communities[comm_tag]
            for fmt in ("std", "lrg", "ext"):
                if comm[fmt]:
                    if comm[fmt] in unique_communities:
                        errors = True
                        logging.error(
                            "The '{}.{}' community's value ({}) "
                            "has already been used for another "
                            "community.".format(comm_tag, fmt, comm[fmt])
                        )
                    else:
                        unique_communities.append(comm[fmt])

        if errors:
            raise ConfigError()
