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

import os
import unittest

import yaml

from .cfg_base import TestConfigParserBase 
from pierky.arouteserver.config.general import ConfigParserGeneral
from pierky.arouteserver.errors import ConfigError


class TestConfigParserGeneric(TestConfigParserBase):

    FILE_PATH = "config.d/general.yml"
    CONFIG_PARSER_CLASS = ConfigParserGeneral

    VALID_STD_COMMS = ("65535:666", "1:1", "0:0", "1:0", "65535:65535", "rs_as:1")
    VALID_LRG_COMMS = ("65535:666:0", "1:1:1", "0:0:0", "1:0:65535", "4294967295:4294967295:4294967295", "rs_as:1:2")
    VALID_EXT_COMMS = ("rt:1:0", "rt:65535:666", "ro:65535:666", "rt:rs_as:3")

    def test_valid_cfg(self):
        """Generic config parser: valid configuration"""
        self._contains_err()

    def test_unknown_statement(self):
        """Generic config parser: unknown statement"""
        self.cfg["test"] = "test"
        self._contains_err("Unknown statement at 'cfg' level: 'test'.")

    def test_rs_as(self):
        """Generic config parser: rs_as"""
        self.assertEqual(self.cfg["rs_as"], 999)
        for asn in (-1, 0, "test"):
            self.cfg["rs_as"] = asn
            self._contains_err("Error parsing 'rs_as' at 'cfg' level - Invalid ASN: {}".format(str(asn)))

        for asn in (1, 65535, 4294967295): 
            self.cfg["rs_as"] = asn
            self._contains_err()

        self._test_mandatory(self.cfg, "rs_as")

    def test_router_id(self):
        """Generic config parser: router_id"""
        self.assertEqual(self.cfg["router_id"], "192.0.2.2")
        for v in ("1.0.0.1", "10.0.0.1"):
            self.cfg["router_id"] = v
            self._contains_err()
        for v in ("10.0.0.1/24", "fe80::1", "2001:db8::1", "test"):
            self.cfg["router_id"] = v
            self._contains_err("Error parsing 'router_id' at 'cfg' level - Invalid IPv4 address: {}.".format(v))
        self._test_mandatory(self.cfg, "router_id")

    def test_prepend_rs_as(self):
        """Generic config parser: prepend_rs_as"""
        self.assertEqual(self.cfg["prepend_rs_as"], False)
        self._test_bool_val(self.cfg, "prepend_rs_as")
        self._test_mandatory(self.cfg, "prepend_rs_as", has_default=True)

    def test_path_hiding(self):
        """Generic config parser: path_hiding"""
        self._test_bool_val(self.cfg, "path_hiding")
        self._test_optional(self.cfg, "path_hiding")

    def test_passive(self):
        """Generic config parser: passive"""
        self.assertEqual(self.cfg["passive"], True)
        self._test_bool_val(self.cfg, "passive")
        self._test_mandatory(self.cfg, "passive", has_default=True)

    def test_gtsm(self):
        """Generic config parser: gtsm"""
        self.assertEqual(self.cfg["gtsm"], False)
        self._test_bool_val(self.cfg, "gtsm")
        self._test_mandatory(self.cfg, "gtsm", has_default=True)

    def test_add_path(self):
        """Generic config parser: add_path"""
        self.assertEqual(self.cfg["add_path"], False)
        self._test_bool_val(self.cfg, "add_path")
        self._test_mandatory(self.cfg, "add_path", has_default=True)

    def test_next_hop_policy(self):
        """Generic config parser: next_hop_policy"""
        self.assertEqual(self.cfg["filtering"]["next_hop_policy"], "strict")
        self._test_option(self.cfg["filtering"], "next_hop_policy", ("strict", "same-as"))
        self._test_mandatory(self.cfg["filtering"], "next_hop_policy", has_default=True)

    def test_ipv4_pref_len(self):
        """Generic config parser: ipv4_pref_len"""
        self.assertEqual(self.cfg["filtering"]["ipv4_pref_len"]["min"], 8)
        self.assertEqual(self.cfg["filtering"]["ipv4_pref_len"]["max"], 24)
        self.cfg["filtering"]["ipv4_pref_len"]["max"] = 32
        self._test_ip_min_max_len(self.cfg["filtering"], "ipv4_pref_len", "min", 4, (0, 1, 32), (-1, 33, "a"))

        self.cfg["filtering"]["ipv4_pref_len"]["min"] = 0
        self._test_ip_min_max_len(self.cfg["filtering"], "ipv4_pref_len", "max", 4, (0, 1, 32), (-1, 33, "a"))

        for pair in ((0, 32), (31, 32), (32, 32)):
            self.cfg["filtering"]["ipv4_pref_len"]["min"] = pair[0]
            self.cfg["filtering"]["ipv4_pref_len"]["max"] = pair[1]
            self._contains_err()
        for pair in ((10, 5), (32, 0)):
            self.cfg["filtering"]["ipv4_pref_len"]["min"] = pair[0]
            self.cfg["filtering"]["ipv4_pref_len"]["max"] = pair[1]
            self._contains_err("Error parsing 'ipv4_pref_len' at 'cfg.filtering' level - In the IPv4 min/max length, the value of 'min' must be <= the value of 'max'.")

    def test_ipv6_pref_len(self):
        """Generic config parser: ipv6_pref_len"""
        self.assertEqual(self.cfg["filtering"]["ipv6_pref_len"]["min"], 12)
        self.assertEqual(self.cfg["filtering"]["ipv6_pref_len"]["max"], 48)
        self.cfg["filtering"]["ipv6_pref_len"]["max"] = 128
        self._test_ip_min_max_len(self.cfg["filtering"], "ipv6_pref_len", "min", 6, (0, 1, 32, 64, 128), (-1, 129, "a"))

        self.cfg["filtering"]["ipv6_pref_len"]["min"] = 0
        self._test_ip_min_max_len(self.cfg["filtering"], "ipv6_pref_len", "max", 6, (0, 1, 32, 64, 128), (-1, 129, "a"))

        for pair in ((0, 64), (32, 48), (32, 32), (128, 128)):
            self.cfg["filtering"]["ipv6_pref_len"]["min"] = pair[0]
            self.cfg["filtering"]["ipv6_pref_len"]["max"] = pair[1]
            self._contains_err()
        for pair in ((10, 5), (32, 0), (128, 0), (128, 64)):
            self.cfg["filtering"]["ipv6_pref_len"]["min"] = pair[0]
            self.cfg["filtering"]["ipv6_pref_len"]["max"] = pair[1]
            self._contains_err("Error parsing 'ipv6_pref_len' at 'cfg.filtering' level - In the IPv6 min/max length, the value of 'min' must be <= the value of 'max'.")

    def test_global_black_list_pref(self):
        """Generic config parser: global_black_list_pref"""

        self.cfg._load_from_yaml(
            "cfg:\n"
            "  rs_as: 999\n"
            "  router_id: 192.0.2.2\n"
            "  filtering:\n"
            "    global_black_list_pref:\n"
            "      - prefix: 192.0.2.0\n"
            "        length: 24\n"
            "        comment: 'Local network'\n"
        )
        self.cfg.parse()
        self._contains_err()

        self.assertEqual(self.cfg["filtering"]["global_black_list_pref"][0],
                         {
                             "prefix": "192.0.2.0",
                             "length": 24,
                             "comment": "Local network",
                             "exact": False,
                             "ge": None,
                             "le": None,
                             "max_length": 32
                         })
        self._test_optional(self.cfg["filtering"], "global_black_list_pref")

    def test_max_as_path_len(self):
        """Generic config parser: max_as_path_len"""
        self.assertEqual(self.cfg["filtering"]["max_as_path_len"], 32)
        for v in (0, 65):
            self.cfg["filtering"]["max_as_path_len"] = v
            self._contains_err("Error parsing 'max_as_path_len' at 'cfg.filtering' level - Invalid max_as_path_len: must be an integer between 1 and 64.")
        for v in (1, 64, 32):
            self.cfg["filtering"]["max_as_path_len"] = v
            self._contains_err()
        self._test_mandatory(self.cfg["filtering"], "max_as_path_len", has_default=True)

    def test_reject_invalid_as_in_as_path(self):
        """Generic config parser: reject_invalid_as_in_as_path"""
        self.assertEqual(self.cfg["filtering"]["reject_invalid_as_in_as_path"], True)
        self._test_bool_val(self.cfg["filtering"], "reject_invalid_as_in_as_path")
        self._test_mandatory(self.cfg["filtering"], "reject_invalid_as_in_as_path", has_default=True)

    def test_tag_as_set(self):
        """Generic config parser: tag_as_set"""
        self.assertEqual(self.cfg["filtering"]["rpsl"]["tag_as_set"], True)
        self._test_bool_val(self.cfg["filtering"]["rpsl"], "tag_as_set")
        self._test_mandatory(self.cfg["filtering"]["rpsl"], "tag_as_set", has_default=True)

    def test_enforce_origin_in_as_set(self):
        """Generic config parser: enforce_origin_in_as_set"""
        self.assertEqual(self.cfg["filtering"]["rpsl"]["enforce_origin_in_as_set"], True)
        self._test_bool_val(self.cfg["filtering"]["rpsl"], "enforce_origin_in_as_set")
        self._test_mandatory(self.cfg["filtering"]["rpsl"], "enforce_origin_in_as_set", has_default=True)

    def test_enforce_prefix_in_as_set(self):
        """Generic config parser: enforce_prefix_in_as_set"""
        self.assertEqual(self.cfg["filtering"]["rpsl"]["enforce_prefix_in_as_set"], True)
        self._test_bool_val(self.cfg["filtering"]["rpsl"], "enforce_prefix_in_as_set")
        self._test_mandatory(self.cfg["filtering"]["rpsl"], "enforce_prefix_in_as_set", has_default=True)

    def test_rpki_enabled(self):
        """Generic config parser: rpki, enabled"""
        self.assertEqual(self.cfg["filtering"]["rpki"]["enabled"], True)
        self._test_bool_val(self.cfg["filtering"]["rpki"], "enabled")
        self._test_mandatory(self.cfg["filtering"]["rpki"], "enabled", has_default=True)

    def test_rpki_data_source(self):
        """Generic config parser: rpki, data_source"""
        self.assertEqual(self.cfg["filtering"]["rpki"]["data_source"], "rtrsub")
        self._test_option(self.cfg["filtering"]["rpki"], "data_source", ("rtrsub", "rtrlib"))
        self._test_optional(self.cfg["filtering"]["rpki"], "data_source")

    def test_rpki_reject_invalid(self):
        """Generic config parser: rpki, reject_invalid"""
        self.assertEqual(self.cfg["filtering"]["rpki"]["reject_invalid"], True)
        self._test_bool_val(self.cfg["filtering"]["rpki"], "reject_invalid")
        self._test_optional(self.cfg["filtering"]["rpki"], "reject_invalid")

    def test_blackhole_announce_to_client(self):
        """Generic config parser: blackhole_filtering, announce_to_client"""
        self.assertEqual(self.cfg["blackhole_filtering"]["announce_to_client"], True)
        self._test_bool_val(self.cfg["blackhole_filtering"], "announce_to_client")

    def test_blackhole_filtering_policy_ipv4(self):
        """Generic config parser: blackhole_filtering, policy_ipv4"""
        self.load_config(file_name="{}/test_cfg_general_blackhole_filtering.yml".format(os.path.dirname(__file__)))
        self.assertEqual(self.cfg["blackhole_filtering"]["policy_ipv4"], "propagate-unchanged")

        self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv4"] = "192.0.2.1"
        self._test_option(self.cfg["blackhole_filtering"], "policy_ipv4", ("propagate-unchanged", "rewrite-next-hop"))
        self._test_optional(self.cfg["blackhole_filtering"], "policy_ipv4")

        self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv4"] = ""
        self.cfg["blackhole_filtering"]["policy_ipv4"] = "propagate-unchanged"
        self._contains_err()
        self.cfg["blackhole_filtering"]["policy_ipv4"] = "rewrite-next-hop"
        self._contains_err("Since blackhole_filtering.policy_ipv4 is 'rewrite_next_hop', an IPv4 address must be provided in 'rewrite_next_hop_ipv4'.")

    def test_blackhole_filtering_policy_ipv6(self):
        """Generic config parser: blackhole_filtering, policy_ipv6"""
        self.load_config(file_name="{}/test_cfg_general_blackhole_filtering.yml".format(os.path.dirname(__file__)))
        self.assertEqual(self.cfg["blackhole_filtering"]["policy_ipv6"], "propagate-unchanged")

        self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv6"] = "fe80::1"
        self._test_option(self.cfg["blackhole_filtering"], "policy_ipv6", ("propagate-unchanged", "rewrite-next-hop"))
        self._test_optional(self.cfg["blackhole_filtering"], "policy_ipv6")

        self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv6"] = ""
        self.cfg["blackhole_filtering"]["policy_ipv6"] = "propagate-unchanged"
        self._contains_err()
        self.cfg["blackhole_filtering"]["policy_ipv6"] = "rewrite-next-hop"
        self._contains_err("Since blackhole_filtering.policy_ipv6 is 'rewrite_next_hop', an IPv6 address must be provided in 'rewrite_next_hop_ipv6'.")

    def test_blackhole_filtering_ipv4(self):
        """Generic config parser: blackhole_filtering, rewrite_next_hop, ipv4"""
        self.load_config(file_name="{}/test_cfg_general_blackhole_filtering.yml".format(os.path.dirname(__file__)))
        for ip in ("127.0.0.1", "192.168.0.1", "192.0.2.1", "12.34.56.78"):
            self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv4"] = ip
            self._contains_err()
        for ip in ("10.0.0.1/24", "a", "fe80::1"):
            self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv4"] = ip
            self._contains_err("Error parsing 'rewrite_next_hop_ipv4' at 'cfg.blackhole_filtering' level - Invalid IPv4 address: {}.".format(ip))
        self._test_optional(self.cfg["blackhole_filtering"], "rewrite_next_hop_ipv4")

    def test_blackhole_filtering_ipv6(self):
        """Generic config parser: blackhole_filtering, rewrite_next_hop, ipv6"""
        self.load_config(file_name="{}/test_cfg_general_blackhole_filtering.yml".format(os.path.dirname(__file__)))
        for ip in ("fe80::1", "2001:DB8::1"):
            self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv6"] = ip
            self._contains_err()
        for ip in ("10.0.0.1/24", "a"):
            self.cfg["blackhole_filtering"]["rewrite_next_hop_ipv6"] = ip
            self._contains_err("Error parsing 'rewrite_next_hop_ipv6' at 'cfg.blackhole_filtering' level - Invalid IPv6 address: {}.".format(ip))
        self._test_optional(self.cfg["blackhole_filtering"], "rewrite_next_hop_ipv6")

    def test_control_communities(self):
        """Generic config parser: control_communities"""
        self.assertEqual(self.cfg["control_communities"], True)
        self._test_bool_val(self.cfg, "control_communities")
        self._test_mandatory(self.cfg, "control_communities", has_default=True)

    def test_communities_std(self):
        """Generic config parser: standard BGP communities"""


        self.cfg["communities"]["blackholing"] = {}
        for c in self.VALID_STD_COMMS:
            self.cfg["communities"]["blackholing"]["std"] = c
            self._contains_err()
        for c in ("65536:666", "-1:-1", "0:-1", "65535:65536", "1", "1:1:1", "rt:1:0") + self.VALID_LRG_COMMS + self.VALID_EXT_COMMS:
            self.cfg["communities"]["blackholing"]["std"] = c
            self._contains_err("Invalid BGP standard community: {};".format(c))
        for c in ("65535:peer_as", "peer_as:1"):
            self.cfg["communities"]["blackholing"]["std"] = c
            self._contains_err("'peer_as' macro not allowed")
        self.cfg["communities"]["blackholing"]["std"] = self.VALID_STD_COMMS[0]
        self._test_optional(self.cfg["communities"]["blackholing"], "std")

    def test_communities_lrg(self):
        """Generic config parser: large BGP communities"""

        for c in self.VALID_LRG_COMMS:
            self.cfg["communities"]["blackholing"]["lrg"] = c
            self._contains_err()
        for c in ("4294967296:1:1", "-1:0:0") + self.VALID_STD_COMMS + self.VALID_EXT_COMMS:
            self.cfg["communities"]["blackholing"]["lrg"] = c
            self._contains_err("Invalid BGP large community: {};".format(c))
        for c in ("1:65535:peer_as", "peer_as:1:1", "1:peer_as:2"):
            self.cfg["communities"]["blackholing"]["lrg"] = c
            self._contains_err("'peer_as' macro not allowed")
        self.cfg["communities"]["blackholing"]["lrg"] = self.VALID_LRG_COMMS[0]
        self._test_optional(self.cfg["communities"]["blackholing"], "lrg")

    def test_communities_ext(self):
        """Generic config parser: extended BGP communities"""

        for c in self.VALID_EXT_COMMS:
            self.cfg["communities"]["blackholing"]["ext"] = c
            self._contains_err()
        for c in ("x:1:0", "ro:-1:0") + self.VALID_STD_COMMS + self.VALID_LRG_COMMS:
            self.cfg["communities"]["blackholing"]["ext"] = c
            self._contains_err("Invalid BGP extended community: {};".format(c))
        for c in ("rt:65535:peer_as", "ro:peer_as:1"):
            self.cfg["communities"]["blackholing"]["ext"] = c
            self._contains_err("'peer_as' macro not allowed")
        self._test_optional(self.cfg["communities"]["blackholing"], "ext")

    def test_fixed_values_communities(self):
        """Generic config parser: communities with fixed values"""

        for comm in ("announce_to_peer", "do_not_announce_to_peer"):
            for c in self.VALID_STD_COMMS:
                self.cfg["communities"][comm]["std"] = c
                self._contains_err("This community must have a fixed value:")
            for c in self.VALID_LRG_COMMS:
                self.cfg["communities"][comm]["lrg"] = c
                self._contains_err("This community must have a fixed value:")
            for c in self.VALID_EXT_COMMS:
                self.cfg["communities"][comm]["ext"] = c
                self._contains_err("This community must have a fixed value:")
            self.cfg["communities"][comm]["std"] = None
            self.cfg["communities"][comm]["lrg"] = None
            self.cfg["communities"][comm]["ext"] = None
            self.cfg.parse()

    def test_duplicate_communities(self):
        """Generic config parser: duplicate communities"""
        tpl = [
            "cfg:",
            "  rs_as: 999",
            "  router_id: 192.0.2.2",
            "  communities:",
            "    prefix_present_in_as_set:",
            "      std: '999:1'",
            "    prefix_not_present_in_as_set:",
            "      lrg: 'rs_as:2:2'",
        ]
        yaml_lines = tpl + [
            "    origin_present_in_as_set:",
            "      std: 'rs_as:1'"
        ]
        self.load_config(yaml="\n".join(yaml_lines))
        self._contains_err("The 'prefix_present_in_as_set.std' community's value (999:1) has already been used for another community.")

        yaml_lines = tpl + [
            "    origin_present_in_as_set:",
            "      lrg: '999:2:2'"
        ]
        self.load_config(yaml="\n".join(yaml_lines))
        self._contains_err("The 'prefix_not_present_in_as_set.lrg' community's value (999:2:2) has already been used for another community.")

    def test_max_pref_action(self):
        """Generic config parser: max_prefix action"""
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["action"], None)
        self._test_option(self.cfg["filtering"]["max_prefix"], "action", ("shutdown", "restart", "block", "warning"))
        self._test_optional(self.cfg["filtering"]["max_prefix"], "action")

    def test_max_pref_peeringdb(self):
        """Generic config parser: max_prefix PeeringDB"""
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["peering_db"], True)
        self._test_bool_val(self.cfg["filtering"]["max_prefix"], "peering_db")
        self._test_optional(self.cfg["filtering"]["max_prefix"], "peering_db")

    def test_max_pref_general_limit_ipv4(self):
        """Generic config parser: max_prefix general_limit_ipv4"""
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["general_limit_ipv4"], 170000)
        self._test_optional(self.cfg["filtering"]["max_prefix"], "general_limit_ipv4")

    def test_max_pref_general_limit_ipv6(self):
        """Generic config parser: max_prefix general_limit_ipv6"""
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["general_limit_ipv6"], 12000)
        self._test_optional(self.cfg["filtering"]["max_prefix"], "general_limit_ipv6")

    def test_default_values(self):
        """Generic config parser: minimal config"""
        self.load_config(yaml="cfg:\n"
            "  rs_as: 999\n"
            "  router_id: 192.0.2.2"
        )
        self.cfg.parse()
        self._contains_err()

        self.assertEqual(self.cfg["prepend_rs_as"], False)
        self.assertEqual(self.cfg["path_hiding"], True)
        self.assertEqual(self.cfg["passive"], True)
        self.assertEqual(self.cfg["gtsm"], False)
        self.assertEqual(self.cfg["add_path"], False)
        self.assertEqual(self.cfg["filtering"]["next_hop_policy"], "strict")
        self.assertEqual(self.cfg["filtering"]["ipv4_pref_len"]["min"], 8)
        self.assertEqual(self.cfg["filtering"]["ipv4_pref_len"]["max"], 24)
        self.assertEqual(self.cfg["filtering"]["ipv6_pref_len"]["min"], 12)
        self.assertEqual(self.cfg["filtering"]["ipv6_pref_len"]["max"], 48)
        self.assertEqual(self.cfg["filtering"]["max_as_path_len"], 32)
        self.assertEqual(self.cfg["filtering"]["reject_invalid_as_in_as_path"], True)
        self.assertEqual(self.cfg["filtering"]["rpsl"]["tag_as_set"], True)
        self.assertEqual(self.cfg["filtering"]["rpsl"]["enforce_origin_in_as_set"], True)
        self.assertEqual(self.cfg["filtering"]["rpsl"]["enforce_prefix_in_as_set"], True)
        self.assertEqual(self.cfg["filtering"]["rpki"]["enabled"], False)
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["action"], None)
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["peering_db"], True)
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["general_limit_ipv4"], 170000)
        self.assertEqual(self.cfg["filtering"]["max_prefix"]["general_limit_ipv6"], 12000)
        self.assertEqual(self.cfg["blackhole_filtering"]["policy_ipv4"], None)
        self.assertEqual(self.cfg["blackhole_filtering"]["policy_ipv6"], None)
        self.assertEqual(self.cfg["control_communities"], True)

