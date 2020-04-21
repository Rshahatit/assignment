from parse_input import parse_input

# should return two properly parsed titles
def test_one_link():
    source = "Mickey Mouse" 
    destination = "https://en.wikipedia.org/wiki/Albert_Einstein"
    true_source = "Mickey Mouse"
    true_destination = "Albert Einstein"
    source = parse_input(source)
    destination = parse_input(destination)
    assert source == true_source
    assert destination == true_destination