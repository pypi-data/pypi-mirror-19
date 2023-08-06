import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

#### count_exact_matches

@t.test(0)
def has_count_exact_matches(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "count_exact_matches")
    test.description = lambda : "definieert de functie count_exact_matches"

@t.passed(has_count_exact_matches)
@t.test(1)
def is_int_count_exact_matches(test):
    test.test = lambda : assertlib.sameType(lib.getFunction("count_exact_matches", _fileName)("a", "a"), 0)
    test.description = lambda : "count_exact_matches geeft een integer terug"

@t.passed(is_int_count_exact_matches)
@t.test(2)
def count_exact_matches_2(test):
    test.test = lambda : assertlib.exact(
        lib.getFunction("count_exact_matches",
        _fileName)("atgacatgcacaagtatgcat", "atgc"), 2)
    test.description = lambda : "count_exact_matches werkt voor invoer 'atgacatgcacaagtatgcat', 'atgc'"

@t.passed(is_int_count_exact_matches)
@t.test(3)
def count_exact_matches_8(test):
    test.test = lambda : assertlib.exact(
        lib.getFunction("count_exact_matches",
        _fileName)("atgacatgcacaagtatgcat", "a"),  8)
    test.description = lambda : "count_exact_matches werkt voor invoer 'atgacatgcacaagtatgcat', 'a'"

@t.passed(is_int_count_exact_matches)
@t.test(4)
def count_exact_matches_0a(test):
    test.test = lambda : assertlib.exact(
        lib.getFunction("count_exact_matches",
        _fileName)("atgacatgcacaagtatgcat", "b"), 0)
    test.description = lambda : "count_exact_matches werkt voor invoer 'atgacatgcacaagtatgcat', 'b'"

@t.passed(is_int_count_exact_matches)
@t.test(5)
def count_exact_matches_0b(test):
    test.test = lambda : assertlib.exact(
        lib.getFunction("count_exact_matches",
        _fileName)("", "atgc"), 0)
    test.description = lambda : "count_exact_matches werkt voor invoer '', 'atgc'"



#### exact_matches

@t.test(6)
def has_exact_matches(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "exact_matches")
    test.description = lambda : "definieert de functie exact_matches"

@t.passed(has_exact_matches)
@t.test(7)
def is_list_exact_matches(test):
    test.test = lambda : assertlib.sameType(lib.getFunction("exact_matches", _fileName)("a", "a"), [])
    test.description = lambda : "exact_matches geeft een lijst terug"

@t.passed(is_list_exact_matches)
@t.test(8)
def exact_matches_a(test):
    test.test = lambda : set(lib.getFunction("exact_matches",
        _fileName)("atgacatgcacaagtatgcat", "atgc")) == set([5,15])
    test.description = lambda : "exact_matches werkt voor invoer 'atgacatgcacaagtatgcat', 'atgc'"

@t.passed(is_list_exact_matches)
@t.test(9)
def exact_matches_b(test):
    test.test = lambda : set(lib.getFunction("exact_matches",
        _fileName)("atgacatgca", "a")) == set([0, 3, 5, 9])
    test.description = lambda : "exact_matches werkt voor invoer 'atgacatgca', 'a'"

@t.passed(is_list_exact_matches)
@t.test(10)
def exact_matches_c(test):
    test.test = lambda : set(lib.getFunction("exact_matches",
        _fileName)("atgacatgca", "b")) == set([])
    test.description = lambda : "exact_matches werkt voor invoer 'atgacatgca', 'b'"

@t.passed(is_list_exact_matches)
@t.test(11)
def exact_matches_c(test):
    test.test = lambda : set(lib.getFunction("exact_matches",
        _fileName)("atgacatgca", "")) == set(range(10))
    test.description = lambda : "exact_matches werkt voor invoer 'atgacatgca', ''"

@t.passed(is_list_exact_matches)
@t.test(12)
def exact_matches_c(test):
    test.test = lambda : set(lib.getFunction("exact_matches",
        _fileName)("", "test")) == set()
    test.description = lambda : "exact_matches werkt voor invoer '', 'test'"






