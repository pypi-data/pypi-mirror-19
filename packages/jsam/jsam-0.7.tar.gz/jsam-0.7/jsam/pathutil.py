# Copyright (C) 2011-2014 by Philip L. Budne
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

"""
Utility routines for JSON object "Paths"
"""

def path_get(obj, path):
    """obj is a JSON object
       path is a list of keys/indices"""

    for idx in path:
        if isinstance(obj, (list, tuple)) and isinstance(idx, basestring):
            obj = obj[int(idx)]
        else:
            obj = obj[idx]

    return obj


def path_set(obj, path, value):
    """modify 'obj' element at 'path' to 'value'
       NOTE: Will not auto-extend non-terminal elements
       (add new hashes, lists, hash-elements or list entries)
       would have to infer list vs hash by path element type.
       """
    obj = path_get(obj, path[:-1])
    idx = path[-1]
    if isinstance(obj, (list, tuple)):
        if isinstance(idx, basestring):
            idx = int(idx)
        # sigh: extend list as needed
        while len(obj) <= idx:
            obj.append(None)
    obj[idx] = value

if __name__ == "__main__":
    def test1():
        obj = { "farmers": {
                "old macdonald": {
                    "cow": "moo",
                    "pig": "oink",
                    "horse": "neigh"
                 }
                }
              }

        print path_get(obj, ["farmers", "old macdonald", "cow" ])
        path_set(obj, ["farmers", "old macdonald", "dog" ], "woof")
        print path_get(obj, ["farmers", "old macdonald", "dog" ])

    def test2():
        obj = { "farms": [
                { "farmer": "old macdonald",
                  "animals": [
                        ["cow", "moo"],
                        ["pig", "oink"],
                        ["horse", "neigh"]
                  ]
                }
                ]
                }

        print path_get(obj, ["farms", 0, "farmer"])
        print path_get(obj, ["farms", 0, "animals", "0"])
        print path_get(obj, ["farms", 0, "animals", 1])

        path_set(obj, ["farms", 0, "animals", 3], [])
        path_set(obj, ["farms", 0, "animals", "3", 0], "turkey")
        path_set(obj, ["farms", 0, "animals", 3, 1], "gobble")
        print path_get(obj, ["farms", 0, "animals", 3])

    test1()
    test2()

