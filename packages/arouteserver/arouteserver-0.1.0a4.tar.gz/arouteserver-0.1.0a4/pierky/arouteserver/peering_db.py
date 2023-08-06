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

import json
import subprocess
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


from .cached_objects import CachedObject
from .errors import PeeringDBError, PeeringDBNoInfoError


class PeeringDBInfo(CachedObject):

    def _get_peeringdb_url(self):
        raise NotImplementedError()

    @staticmethod
    def _read_from_url(url):
        try:
            response = urlopen(url)
        except Exception as e:
            raise PeeringDBError(
                "Error while retrieving info from PeeringDB: {}".format(
                    str(e)
                )
            )

        return response.read().decode("utf-8")

    def _get_data_from_peeringdb(self):
        plain_text = self._read_from_url(self._get_peeringdb_url())
        try:
            data = json.loads(plain_text)
            return data
        except Exception as e:
            raise PeeringDBError(
                "Error while decoding PeeringDB output: {}".format(
                    str(e)
                )
            )

class PeeringDBNet(PeeringDBInfo):

    PEERINGDB_URL = "https://www.peeringdb.com/api/net?asn={asn}"

    def __init__(self, asn, **kwargs):
        PeeringDBInfo.__init__(self, **kwargs)
        self.asn = asn
        self.load_data()
    
        self.info_prefixes4 = self.raw_data.get("info_prefixes4", None)
        self.info_prefixes6 = self.raw_data.get("info_prefixes6", None)

    def _get_object_filename(self):
        return "peeringdb_net_{}.json".format(self.asn)

    def _get_peeringdb_url(self):
        return self.PEERINGDB_URL.format(asn=self.asn)

    def _get_data(self):
        data = self._get_data_from_peeringdb()
        if not "data" in data:
            raise PeeringDBNoInfoError("Missing 'data'")
        if not isinstance(data["data"], list):
            raise PeeringDBNoInfoError("Unexpected format: 'data' is not a list")
        if len(data["data"]) == 0:
            raise PeeringDBNoInfoError("No data for this nextwork")

        return data["data"][0]
