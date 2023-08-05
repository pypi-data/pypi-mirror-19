# Copyright 2017 Josh Fischer

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
from contextlib import contextmanager
from restructure.printer import Printer


class TestPrinter(TestCase):

	def test_1_is_1(self):
		printer = Printer()
		str_to_test = 'some string'
		self.assertTrue(isinstance(str_to_test, basestring))