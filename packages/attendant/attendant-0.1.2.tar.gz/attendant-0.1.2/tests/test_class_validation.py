"""
Module for testing validation.py

This module si for testing each use case for the validations
Since the main class Validation to the sub classes and the
validate function with this two cases.
"""
import pytest
from attendant.validation import Validation, Multivalue, MultivalueAll, Univalue, UnivaluePosType, validate

def test_call_classMultivalue_pass():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	assert callable(a)


def test_Multivalue_pass():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	assert a("0, 1", int) == ''

def test_Multivalue_fail():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	assert a("0,4,6", int) == '0 or/and 1 was invalid'


def test_Multivalue_fail2():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	assert a("0,1", str) == '0 or/and 1 was invalid'


def test_call_classMultivalueAll_pass():
	a = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	assert callable(a)


def test_MultivalueAll_pass():
	a = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	assert a("0,all", int) == ''


def test_MultivalueAll_pass1():
	a = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	assert a("all", int) == ''


def test_MultivalueAll_fail():
	a = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	assert a("0,4,and", int) == "0 or/and 1 or/and all was invalid"


def test_MultivalueAll_fail2():
	a = MultivalueAll(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	assert a("0,1,all", str) == '0 or/and 1 was invalid'


def test_call_classUnivalue_pass():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	b = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert callable(a)
	assert callable(b)


def test_Univalue_pass():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	assert a(0, int) == ''


def test_Univalue_pass2():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	assert a(1, int) == ''
	

def test_Univalue_fail():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	assert a("hello", str) == "0 or 1 was invalid"


def test_Univalue_fail2():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	assert a("0,1", int) == "0 or 1 was invalid"


def test_Univalue_fail3():
	a = Univalue(lambda x: x in (0,1), "0 or 1")
	assert a(3, int) == "0 or 1 was invalid"


def test_Univalue_str_pass():
	a = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert a("hola", str) == ''


def test_Univalue_str_pass2():
	a = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert a("adios", str) == ''


def test_Univalue_str_fail():
	a = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert a("hol", str) == "hola or adios was invalid"


def test_Univalue_str_fail1():
	a = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert a(2, str) == "hola or adios was invalid"


def test_Univalue_str_fail2():
	a = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	assert a(3, int) == "hola or adios was invalid"


def test_call_classUnivaluePosType_pass():
	a = UnivaluePosType("positive or type")
	assert callable(a)


def test_UnivaluePosType_pass():
	a = UnivaluePosType("positive or type")
	assert a(1, int) == ''


def test_UnivaluePosType_pass2():
	a = UnivaluePosType("positive or type")
	assert a("hello", str) == ''


def test_UnivaluePosType_fail():
	a = UnivaluePosType("positive or type")
	assert a(-1, int) == 'positive or type was invalid'


def test_UnivaluePosType_fail2():
	a = UnivaluePosType("positive or type")
	assert a("bye", int) == 'positive or type was invalid'


def test_validate_Multiclass_pass():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	b = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	c = Univalue(lambda x: x in (0,1), "0 or 1")
	d = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	e = UnivaluePosType("positive or type")

	params = {
		"0 or/and 1": ["0", int],
		"0 or/and 1 or/and all": ["1,all", int],
		"0 or 1": [1, int],
		"hola or adios": ["hola", str],
		"positive or type": [6, int]
	}

	schema = {
		"0 or/and 1": a,
		"0 or/and 1 or/and all": b,
		"0 or 1": c,
		"hola or adios": d,
		"positive or type": e
	}

	errors = validate(schema, params)
	assert len(errors) == 0


def test_validate_Multiclass_fail():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	b = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	c = Univalue(lambda x: x in (0,1), "0 or 1")
	d = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	e = UnivaluePosType("positive or type")

	params = {
		"0 or/and 1": ["0", int],
		"0 or/and 1 or/and all": ["1,all", int],
		"0 or 1": [1, int],
		"hola or adios": ["hola", int],
		"positive or type": [6, int]
	}

	schema = {
		"0 or/and 1": a,
		"0 or/and 1 or/and all": b,
		"0 or 1": c,
		"hola or adios": d,
		"positive or type": e
	}

	errors = validate(schema, params)
	assert len(errors) == 1
	assert errors == {'hola or adios': 'hola or adios was invalid'}


def test_validate_Multiclass_fail2():
	a = Multivalue(lambda xs: all(x in (0, 1) for x in xs), "0 or/and 1")
	b = MultivalueAll(lambda xs: all(x in (0, 1, "all") for x in xs), "0 or/and 1 or/and all")
	c = Univalue(lambda x: x in (0,1), "0 or 1")
	d = Univalue(lambda x: x in ("hola","adios"), "hola or adios")
	e = UnivaluePosType("positive or type")

	params = {
		"0 or/and 1": ["0", int],
		"0 or/and 1 or/and all": ["1,all", int],
		"0 or 1": [1, int],
		"hola or adios": ["hola", str],
		"positive or type": [-6, int]
	}

	schema = {
		"0 or/and 1": a,
		"0 or/and 1 or/and all": b,
		"0 or 1": c,
		"hola or adios": d,
		"positive or type": e
	}

	errors = validate(schema, params)
	assert len(errors) == 1
	assert errors == {'positive or type': 'positive or type was invalid'}