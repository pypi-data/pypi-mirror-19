# -*- coding: utf-8 -*-
from z3c.form.testing import TestRequest


class BaseTestRequest(TestRequest):

    @property
    def REQUEST_METHOD(self):
        return self.method
