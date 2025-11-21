API_KEY = "API_KEY"

subject_description = 'An entity being described. It is typically a noun, such as a person, a place, a concept, or an object.'
predicate_description = 'Property or the relationship that describes the Subject. It is almost always a verb or a characteristic trait.'
object_description =  'The value or the "target" of the relationship. It can be another entity (like the Subject) or a literal value (like a number, string, or date)'

min_amt_triplets = 2

sys_extr_prompt = "You create knowledge base which consists out of triplets. Construct triplet out of given text. Try not to make triplets complex, so Subject, Predicate and Object will be at most three words"
sys_answ_prompt = "You must give an id of the question answer on this question based on the given knowledge base consisting of triplets. On each question give answer, which must consist out of one word"
get_tr_amt_prompt = f'You need to create knowledge base consisting of triplets for given text to later answer any possible question about this text correctly. How many triplets do you need? Minimum number of triplets is {min_amt_triplets}'

models = ['gpt-3.5-turbo','gpt-4-turbo', 'gpt-5-chat-latest']

functions = [
    {
        'name': 'extract_triplet',
        'description': 'Get the meaningful triplet for knowledge base based on the text',
        'parameters': {
            'type': 'object',
            'properties': {
                'Subject': {
                    'type': 'string',
                    'description': subject_description
                },
                'Predicate': {
                    'type': 'string',
                    'description': predicate_description
                },
                'Object': {
                    'type': 'string',
                    'description': object_description
                }
            },
            "required": ['Subject', 'Predicate', 'Object']
        }
    },

    {
        'name': 'get_amt_triplet',
        'description': 'Give number of triplets which is necessary to create knowledge base based on this text',
        'parameters': {
            'type': 'object',
            'properties': {
                'number of triplets': {
                    'type': 'integer',
                    'description': "Number of triplets which is necessary to create knowledge base"
                }
            },
            "required": ['number of triplets']
        }
    },

    {
        'name': 'answer_question',
        'description': 'Give an number of question and answer the question. An answer must be one word',
        'parameters': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'integer',
                    'description': 'number of the question'
                },
                'answer': {
                    'type': 'string',
                    'description':'An answer on the question. An answer must be one word'
                }
            },
            "required": ['id', 'answer']
        }
    }
]
