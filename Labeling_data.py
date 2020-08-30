import pandas as pd
answers = pd.read_csv('Local_Answers_v_0_9_1.csv')
numerical_indexes = [1, 5, 6, 8, 9, 10, 11, 18]
intents = ['diag', 'cam', 'os', 'ram', 'rom', 'weight', 'acc', 'sim']
numerical_answers = answers.iloc[:, numerical_indexes]
numerical_answers.columns = intents
result = pd.DataFrame()


def get_number_from_statement(phrase):
    res = '-'
    for word in phrase.split():
        try:
            res = float(word.replace(',', '.'))
        except ValueError:
            pass
    return res


def get_dimension_from_statement(phrase):
    res = '-'
    number = False
    for word in phrase.split():
        if number:
            res = word
            break
        try:
            float(word)
            number = True
        except ValueError:
            pass
    return res


numbers = []
dimensions = []
texts = []
is_answer = []
intents_for_result = []

for intent in intents:
    for statement in numerical_answers.loc[:, intent].values:
        numbers.append(get_number_from_statement(statement))
        dimensions.append(get_dimension_from_statement(statement))
        texts.append(statement)
        if get_number_from_statement(statement) == '-':
            is_answer.append(0)
        else:
            is_answer.append(1)
        intents_for_result.append(intent)

result['Интент'] = intents_for_result
result['Текст'] = texts
result['Число'] = numbers
result['Размерность'] = dimensions
result['Нет ответа'] = is_answer

result.to_csv('result.csv', encoding='windows-1251')
