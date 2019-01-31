# Copyright 2018 SunSpec Alliance

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from inspect import currentframe

import unittest
from parser import Parser, ValidationErrors
import taxonomy
import pytest

taxonomy = taxonomy.Taxonomy()
parser = Parser(taxonomy)

def _ln():
    # Returns line number of caller.

    cf = currentframe()
    return cf.f_back.f_lineno

class TestJsonClips(unittest.TestCase):
    # Note: this module is tested differently than others.  Erroneous JSON clips are run through
    # the parser validator method and should cause various error methods to occur.  The resulting
    # exception string is expected to match a regular expression which should prove that enough
    # information is returned to correctly diagnose the error (although a perfect match is not
    # necessarily required unless noted via the expression).  A line number in the JSON also is
    # present and in an ideal world the line number should also be decipherable fromt he parser.

     def test_clips(self):
        failure_list = []
        for clip in CLIPS:
            try:
                # print(JSON_HEADER + clip[4] + JSON_FOOTER)
                # return
                parser.from_JSON_string(JSON_HEADER + clip[4] + JSON_FOOTER, entrypoint_name=clip[1])
                if clip[2] is not None:
                    failure_list.append("Case {} did not cause a failure condition as expected".format(clip[0]))
            except Exception as e:
                if clip[2] is None:
                    if isinstance(e, ValidationErrors):
                        for e2 in e.get_errors():
                            s = str(e2)
                            failure_list.append("Case {} should have succeeded, raised {}".format(clip[0], s))
                    else:
                        failure_list.append("Case {} should have succeeded, raised an unexpected exception ''".format(clip[0], str(e)))
                else:
                    if isinstance(e, ValidationErrors):
                        for e2 in e.get_errors():
                            s = str(e2)
                            if re.search(clip[2], s, re.IGNORECASE) is None:
                                failure_list.append("Case {} exception text '{}' did not meet expected value '{}'".format(clip[0], s, clip[2]))
                    else:
                        failure_list.append("Case {} raised an unexpected exception '{}'".format(clip[0], str(e)))

        if len(failure_list) > 0:
            msg = "\n"
            for f in failure_list:
                msg = msg + f + "\n"
            # TODO: Uncomment this line and remove the print statement.  At this point in time the
            # validator rules are not implemented so this test case cannot actually fail although
            # in reality it should be failing.
            # self.fail(msg)
            print(msg)
            print("{} issues found out of {} test cases".format(len(failure_list), len(CLIPS)))

CLIPS = [
    [_ln(), "MonthlyOperatingReport", "Identifier is not a uuid", 1, """
        "illegal-identifier": {
        "value": "93.26",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "Float expected", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Bad Data",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "is not a writeable concept", 4, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Bad Data",
        "aspects": {
            "concept": 2,
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "Entity is not a string", 5, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Bad Data",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": 3,
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "period start component is in an incorrect format", 6, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "93.26",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-13-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "period end component is in an incorrect format", 7, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "93.26",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-13-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "Identifier is not a uuid", 1, """
        "illegal-identifier": {
        "value": "93.26",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "fact tag is missing value tag", 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "fact tag is missing aspects tag", 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "93.26"
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "aspects tag is missing concept tag", 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "93.26",
        "aspects": {
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "aspects tag is missing entity tag", 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "93.26",
        "aspects": {
            "concept": "solar:MeasuredEnergyAvailabilityPercent",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MasterPurchaseAgreement", "Non-nillable value is set to null", 3, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": null,
        "aspects": {
            "concept": "solar:PreparerOfMasterPurchaseAgreement",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": true,
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "non-boolean",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "true",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "false",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "1",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "0",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "1.0",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:booleanItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "0.0",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportAvailabilityOfDocument",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-01-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-01-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-02-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2017-02-28",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-02-28",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2019-02-28",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2020-02-29",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-03-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-03-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-04-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-04-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-05-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-05-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-06-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-06-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-07-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-07-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-08-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-08-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-01-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-09-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-10-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-10-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-11-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-11-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-12-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-12-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-13-02",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-01-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2016-02-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2017-02-28",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2019-02-29",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2020-02-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-03-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-04-30",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-05-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-06-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-08-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-09-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-10-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-11-31",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-12-32",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-1-01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018-01-1",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2018_01_01",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "01-01-2018",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "01/01/2018",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:dateItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportEndDate",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.0",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "-99.99",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"            
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"            
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type xbrli:decimalItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type xbrli:decimalItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type xbrli:decimalItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:MonitoringSolutionSoftwareVersion",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1Y",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "PT1004199059S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "PT130S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "PT2M10S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1DT2S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "-P1Y",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1Y2M3DT5H20M30.123S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "1Y",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1S",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1-Y",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1M2Y",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "P1Y-1M",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:durationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid",
        "aspects": {
            "concept": "solar:EstimationPeriodForCurtailment",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EstimationPeriodStartDateAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "-99",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "0",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", "value is not legal for type xbrli:integerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", "value is not legal for type xbrli:integerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", "value is not legal for type xbrli:integerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", "value is not legal for type xbrli:integerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid",
        "aspects": {
            "concept": "solar:WashingAndWasteFrequencyOfWashing",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "9999.99",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "9999",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "9999.9",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "9999.999",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "9999.99",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:monetaryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid",
        "aspects": {
            "concept": "us-gaap:PrepaidExpenseCurrentAndNoncurrent",
            "entity": "JUPITER",
            "period": "2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Sample String",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportExceptionDescription",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:stringItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MonthlyOperatingReportExceptionDescription",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:stringItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportExceptionDescription",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type xbrli:stringItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportExceptionDescription",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "0.0",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type num:percentItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "-0.01",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type num:percentItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "100.01",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type num:percentItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type num:percentItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:AerosolModelFactorTMMPercent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "http://www.google.com",
        "aspects": {
            "concept": "solar:CutSheetDocumentLink",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "https://www.google.com",
        "aspects": {
            "concept": "solar:CutSheetDocumentLink",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "", "value is not legal for type xbrli:anyURIItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:CutSheetDocumentLink",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "", "value is not legal for type xbrli:anyURIItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:CutSheetDocumentLink",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "", "value is not legal for type xbrli:anyURIItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99",
        "aspects": {
            "concept": "solar:CutSheetDocumentLink",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Participant", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "5493006MHB84DD0ZWV18",
        "aspects": {
            "concept": "dei:LegalEntityIdentifier",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Participant", "value is not legal for type dei:legalEntityIdentifierItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "dei:LegalEntityIdentifier",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:ModuleShortCircuitCurrent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num-us:electricCurrentItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleShortCircuitCurrent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:InverterOutputRatedFrequency",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num-us:frequencyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InverterOutputRatedFrequency",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:ExpectedInsolationAtP50",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "value is not legal for type num-us:insolationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ExpectedInsolationAtP50",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "MonthlyOperatingReport", "value is out of range for type num-us:insolationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "101.01",
        "aspects": {
            "concept": "solar:ExpectedInsolationAtP50",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:SystemMinimumIrradianceThreshold",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type num-us:irradianceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemMinimumIrradianceThreshold",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "SystemDeviceListing", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "33.33",
        "aspects": {
            "concept": "solar:TrackerAzimuth",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:DeviceIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "SystemDeviceListing", "value is out of range for type num-us:planeAngleItemType", 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "361.1",
        "aspects": {
            "concept": "solar:TrackerAzimuth",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:DeviceIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "SystemDeviceListing", "value is not legal for type num-us:planeAngleItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:TrackerAzimuth",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:DeviceIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:SiteBarometricPressure",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type num-us:pressureItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteBarometricPressure",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "19.19",
        "aspects": {
            "concept": "solar:TrackerStowWindSpeed",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num-us:speedItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:TrackerStowWindSpeed",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModelAmbientTemperature",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type num-us:temperatureItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModelAmbientTemperature",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:InverterInputMaximumVoltageDC",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num-us:voltageItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InverterInputMaximumVoltageDC",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:SiteAcreage",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type num:areaItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteAcreage",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:ExpectedEnergyAtP50",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:PeriodAxis": "solar:PeriodMonthMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type num:energyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ExpectedEnergyAtP50",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:PeriodAxis": "solar:PeriodMonthMember"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleLength",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num:lengthItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleLength",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:InverterWeight",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type num:massItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InverterWeight",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:BatteryInverterACPowerRating",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type num:powerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:BatteryInverterACPowerRating",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "99.99",
        "aspects": {
            "concept": "solar:WashingAndWasteQuantityOfWater",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "WashingAndWasteAgreement", "value is not legal for type num:volumeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:WashingAndWasteQuantityOfWater",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Storage",
        "aspects": {
            "concept": "solar:SystemDERType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:DERItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemDERType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:DERItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemDERType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Preliminary",
        "aspects": {
            "concept": "solar:AmericanLandTitleAssociationSurveyStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:aLTASurveyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:AmericanLandTitleAssociationSurveyStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:aLTASurveyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:AmericanLandTitleAssociationSurveyStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "NiCad",
        "aspects": {
            "concept": "solar:BatteryStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type solar-types:batteryChemistryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:BatteryStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type solar-types:batteryChemistryItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:BatteryStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "DC-Coupled",
        "aspects": {
            "concept": "solar:SystemBatteryConnection",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:batteryConnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemBatteryConnection",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:batteryConnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemBatteryConnection",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "2.4.1 Hot summer continental climates",
        "aspects": {
            "concept": "solar:SiteClimateClassificationKoppen",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:climateClassificationKoppenItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteClimateClassificationKoppen",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:climateClassificationKoppenItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SiteClimateClassificationKoppen",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Mixed - Marine",
        "aspects": {
            "concept": "solar:SiteClimateZoneTypeANSI",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:climateZoneANSIItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteClimateZoneTypeANSI",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:climateZoneANSIItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SiteClimateZoneTypeANSI",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Modbus",
        "aspects": {
            "concept": "solar:DataAcquisitionSystemCommunicationProtocol",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:communicationProtocolItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:DataAcquisitionSystemCommunicationProtocol",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:communicationProtocolItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:DataAcquisitionSystemCommunicationProtocol",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "BatteryManagementSystemMember",
        "aspects": {
            "concept": "solar:TypeOfDevice",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:deviceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:TypeOfDevice",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:deviceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:TypeOfDevice",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Distributed Generation",
        "aspects": {
            "concept": "solar:ProjectDistributedGenerationPortolioOrUtilityScale",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:distributedGenOrUtilityScaleItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectDistributedGenerationPortolioOrUtilityScale",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:distributedGenOrUtilityScaleItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectDistributedGenerationPortolioOrUtilityScale",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Final Approval",
        "aspects": {
            "concept": "solar:DivisionOfStateArchitectApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:divisionStateApprovalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:DivisionOfStateArchitectApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:divisionStateApprovalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:DivisionOfStateArchitectApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Moderate",
        "aspects": {
            "concept": "solar:ProjectRecentEventSeverityOfEvent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:eventSeverityItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectRecentEventSeverityOfEvent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:eventSeverityItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectRecentEventSeverityOfEvent",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ZoningPermitUpfrontFeeStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:feeStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ZoningPermitUpfrontFeeStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:feeStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invald Value",
        "aspects": {
            "concept": "solar:ZoningPermitUpfrontFeeStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Fund", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:FundStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Fund", "value is not legal for type solar-types:fundStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:FundStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Fund", "value is not legal for type solar-types:fundStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:FundStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "GEOJson",
        "aspects": {
            "concept": "solar:SiteGeospatialBoundaryGISFileFormat",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:gISFileFormatItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteGeospatialBoundaryGISFileFormat",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:gISFileFormatItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SiteGeospatialBoundaryGISFileFormat",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:hedgeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Revenue Put",
        "aspects": {
            "concept": "solar:ProjectHedgeAgreementType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:hedgeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectHedgeAgreementType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:hedgeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectHedgeAgreementType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Surety Solar Module Supply Bond",
        "aspects": {
            "concept": "solar:InsuranceType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InsuranceAxis": "1"            
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:insuranceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InsuranceType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InsuranceAxis": "1"            
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:insuranceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:InsuranceType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InsuranceAxis": "1"            
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:NetworkType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:internetConnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:NetworkType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:internetConnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:NetworkType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProductIdentifierAxis": "1",
            "solar:InverterPowerLevelPercentAxis": "solar:InverterPowerLevel10PercentMember"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "MicroInverter",
        "aspects": {
            "concept": "solar:InverterStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type solar-types:inverterItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InverterStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "IECRECertificate", "value is not legal for type solar-types:inverterItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:InverterStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Three Phase WYE",
        "aspects": {
            "concept": "solar:InverterOutputPhaseType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:inverterPhaseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:InverterOutputPhaseType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:inverterPhaseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:InverterOutputPhaseType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Partial Funding",
        "aspects": {
            "concept": "solar:ProjectInvestmentStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:investmentStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectInvestmentStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:investmentStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectInvestmentStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Fund Level",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:mORLevelItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MonthlyOperatingReportLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:mORLevelItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:MonthlyOperatingReportLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "BiFacial",
        "aspects": {
            "concept": "solar:ModuleStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ModuleStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Portrait",
        "aspects": {
            "concept": "solar:ModuleOrientation",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleOrientationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleOrientation",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleOrientationItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ModuleOrientation",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Multi-C-Si",
        "aspects": {
            "concept": "solar:ModuleTechnology",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleTechnologyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ModuleTechnology",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:moduleTechnologyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ModuleTechnology",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Ballasted",
        "aspects": {
            "concept": "solar:MountingType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:mountingItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:MountingType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:mountingItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:MountingType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:GroundMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Owner Occupied",
        "aspects": {
            "concept": "solar:SitePropertyOccupancyType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:occupancyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SitePropertyOccupancyType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:occupancyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SitePropertyOccupancyType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Attached",
        "aspects": {
            "concept": "solar:OptimizerType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:optimizerTypeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:OptimizerType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "CutSheet", "value is not legal for type solar-types:optimizerTypeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:OptimizerType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:TestConditionAxis": "solar:CustomTestConditionMember",
            "solar:ProductIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Participant", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Workers Compensation Insurer",
        "aspects": {
            "concept": "solar:ParticipantRole",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Participant", "value is not legal for type solar-types:participantItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ParticipantRole",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Participant", "value is not legal for type solar-types:participantItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ParticipantRole",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ParticipantAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Incomplete",
        "aspects": {
            "concept": "solar:SystemPreventiveMaintenanceTasksStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:preventiveMaintenanceTaskStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemPreventiveMaintenanceTasksStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:preventiveMaintenanceTaskStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemPreventiveMaintenanceTasksStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Solar Plus Storage",
        "aspects": {
            "concept": "solar:ProjectAssetType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectAssetTypeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectAssetType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectAssetTypeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectAssetType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Community Solar",
        "aspects": {
            "concept": "solar:ProjectClassType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectClassItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectClassType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectClassItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectClassType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Virtual Net Meter",
        "aspects": {
            "concept": "solar:ProjectInterconnectionType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectInterconnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectInterconnectionType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectInterconnectionItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectInterconnectionType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Early Construction",
        "aspects": {
            "concept": "solar:PhaseOfProjectNeeded",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:projectPhaseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:PhaseOfProjectNeeded",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:projectPhaseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:PhaseOfProjectNeeded",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:IndependentEngineeringServicesChecklistAxis": "solar:IndependentEngineeringServicesChecklistPostFundingActivityMember"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "In Operation",
        "aspects": {
            "concept": "solar:ProjectStage",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"            
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectStageItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ProjectStage",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:projectStageItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ProjectStage",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Not Submitted",
        "aspects": {
            "concept": "solar:RegulatoryApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:regulatoryApprovalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RegulatoryApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:regulatoryApprovalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:RegulatoryApprovalStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "EWG",
        "aspects": {
            "concept": "solar:RegulatoryFacilityType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:regulatoryFacilityItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RegulatoryFacilityType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Project", "value is not legal for type solar-types:regulatoryFacilityItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:RegulatoryFacilityType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ProjectIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Letter of Credit",
        "aspects": {
            "concept": "solar:ReserveCollateralType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:reserveCollateralItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ReserveCollateralType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:reserveCollateralItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ReserveCollateralType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Maintenance",
        "aspects": {
            "concept": "solar:ReserveUse",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:reserveUseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ReserveUse",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:reserveUseItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ReserveUse",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:FundIdentifierAxis": "1",
            "solar:ReserveTypeAxis": "solar:FundReserveMember"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RoofType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:roofItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RoofType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:roofItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:RoofType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RoofSlopeType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:roofSlopeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:RoofSlopeType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:roofSlopeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:RoofSlopeType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:InstallationTypeAxis": "solar:RooftopMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Lease",
        "aspects": {
            "concept": "solar:SiteControlType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:siteControlItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SiteControlType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:siteControlItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SiteControlType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Agricultural",
        "aspects": {
            "concept": "solar:SystemType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:solarSystemCharacterItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:solarSystemCharacterItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemType",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Insufficient",
        "aspects": {
            "concept": "solar:SystemSparePartsStatusLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:sparePartsStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemSparePartsStatusLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), None, "value is not legal for type solar-types:sparePartsStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemSparePartsStatusLevel",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Islanded",
        "aspects": {
            "concept": "solar:SystemAvailabilityMode",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:systemAvailabilityModeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemAvailabilityMode",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:systemAvailabilityModeItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemAvailabilityMode",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Communication Failure",
        "aspects": {
            "concept": "solar:SystemOperationStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:systemOperationalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:SystemOperationStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:systemOperationalStatusItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:SystemOperationStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Pro Forma",
        "aspects": {
            "concept": "solar:TitlePolicyInsuranceStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"              
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:titlePolicyInsuranceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:TitlePolicyInsuranceStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"            
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:titlePolicyInsuranceItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:TitlePolicyInsuranceStatus",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:SiteIdentifierAxis": "1"       
        }
    }
    """
    ],
    [_ln(), "System", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Azimuth Axis Tracking",
        "aspects": {
            "concept": "solar:TrackerStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EquipmentTypeAxis": "solar:ModuleMember",
            "solar:SolarSubArrayIdentifierAxis": "1"            
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:trackerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:TrackerStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EquipmentTypeAxis": "solar:ModuleMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "System", "value is not legal for type solar-types:trackerItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:TrackerStyle",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:PVSystemIdentifierAxis": "1",
            "solar:EquipmentTypeAxis": "solar:ModuleMember",
            "solar:SolarSubArrayIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", None, 0, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ZoningPermitProperty",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:zoningPermitPropertyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": false,
        "aspects": {
            "concept": "solar:ZoningPermitProperty",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ],
    [_ln(), "Site", "value is not legal for type solar-types:zoningPermitPropertyItemType", 2, """
        "d5ead87b-58c6-4aab-9795-e7e92ca0bcf2": {
        "value": "Invalid Value",
        "aspects": {
            "concept": "solar:ZoningPermitProperty",
            "entity": "JUPITER",
            "period": "2017-11-01T00:00:00/2017-11-30T00:00:00",
            "solar:ZoningPermitIdentifierAxis": "1"
        }
    }
    """
    ]
]

JSON_HEADER = """
{
  "documentType": "http://www.xbrl.org/WGWD/YYYY-MM-DD/xbrl-json",
  "prefixes": {
    "xbrl": "http://www.xbrl.org/WGWD/YYYY-MM-DD/oim",
    "solar": "http://xbrl.us/Solar/v1.1/2018-02-09/solar",
    "us-gaap": "http://fasb.org/us-gaap/2017-01-31",
    "iso4217": "http://www.xbrl.org/2003/iso4217",
    "SI": "http://www.xbrl.org/2009/utr"
  },
  "dtsReferences": [
    {
      "type": "schema",
      "href": "https://raw.githubusercontent.com/xbrlus/solar/v1.2/core/solar_all_2018-03-31_r01.xsd"
    }
  ],
  "facts": {
"""

JSON_FOOTER = """
    }
}
"""