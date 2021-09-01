# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, unittest

class Tests():
    def suite(self):
        modules_to_test = []
        test_dir = os.listdir('.')
        for test in test_dir:
            if test.startswith('test') and test.endswith('.py'):
                modules_to_test.append(test.rstrip('.py'))

        alltests = unittest.TestSuite()
        for module in map(__import__, modules_to_test):
            alltests.addTest(unittest.findTestCases(module))
        return alltests

if __name__ == '__main__':
    MyTests = Tests()
    unittest.main(defaultTest='MyTests.suite', verbosity=2)