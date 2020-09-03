import pandas as pd
answers = pd.read_csv('Local_Answers_v_0_9_2.csv')
numerical_indexes = [1, 5, 6, 8, 9, 10, 11, 18]
intents = ['diag', 'cam', 'os', 'ram', 'rom', 'weight', 'acc', 'sim']
dims = {
    'diag': 'дюйм',
    'cam': 'мегапиксель',
    'os': 'android',
    'ram': 'гигабайт',
    'rom': 'гигабайт',
    'weight': 'грамм',
    'acc': 'миллиампер',
    'sim': 'симкарта'
}
numerical_answers = answers.iloc[:, numerical_indexes]
numerical_answers.columns = intents


def get_slots(phrase):
    res_num = []
    res_dim = []
    tokens_ids = []
    tokens = []
    number = False
    for token_id, word in enumerate(phrase.split()):
        tokens_ids.append(token_id)
        tokens.append(word)
        if number:
            res_dim.append('B')
        else:
            res_dim.append('O')
        number = False
        try:
            float(word.replace(',', '.'))
            number = True
            res_num.append('B')
        except ValueError:
            res_num.append('O')
    return res_num, res_dim, tokens_ids, tokens


result = pd.DataFrame()
statement_ids = []
tokens_ids_main = []
tokens_main = []
num_slots = []
dim_slots = []

for intent in intents:
    for statement_id, statement in enumerate(numerical_answers.loc[:, intent].values):
        res_num_current, res_dim_current, tokens_ids_current, tokens_current = get_slots(statement)
        for i in range(len(res_num_current)):
            statement_ids.append(statement_id)
        tokens_ids_main.append(tokens_ids_current)
        tokens_main.append(tokens_current)
        num_slots.append(res_num_current)
        dim_slots.append(res_dim_current)

result['ID'] = statement_ids
result['token_id'] = sum(tokens_ids_main, [])
result['token'] = sum(tokens_main, [])
result['num_slot'] = sum(num_slots, [])
result['dim_slot'] = sum(dim_slots, [])
result.to_csv('result.csv', encoding='windows-1251', index=False)
