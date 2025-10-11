import os
from mem0 import Memory

# os.environ["OPENAI_API_KEY"] = "your-api-key"

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": os.environ.get('QDRANT_HOST'),
            "api_key": os.environ.get('QDRANT_API_KEY'),
            "port": 6333
        },
        "check_compatibility": False

    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "qwen-plus-2025-04-28",
            "openai_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # Custom base URL
            "temperature": 0.2,
            "max_tokens": 2000,
            "api_key": os.environ.get('OPENAI_API_KEY')
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-v4",
            "openai_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # Custom base URL
            "api_key": os.environ.get('OPENAI_API_KEY')
        }
    }
}

m = Memory.from_config(config)


# Store raw messages without inference
# result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"}, infer=False)

def add_memory(message, user_id, speaker_id, receiver_id):
    # Store inferred memories (default behavior)
    result = m.add(message, user_id=user_id, speaker_id=speaker_id, receiver_id=receiver_id)
    return result


def get_all_memories(user_id, speaker_id, receiver_id):
    # Get all memories
    all_memories = m.get_all(user_id = user_id, speaker_id = speaker_id, receiver_id = receiver_id)

    return all_memories


def search_memories(message, user_id, receiver_id, speaker_id):

    related_memories = m.search(query=message, user_id=user_id, receiver_id=receiver_id, speaker_id=speaker_id)
    return related_memories

def delete_all(user_id : str, speaker_id='', receiver_id=''):
    if user_id and speaker_id and receiver_id:
        m.delete_all(user_id=user_id, speaker_id=speaker_id, receiver_id=receiver_id)
    elif user_id:
        m.delete_all(user_id=user_id)

def delete(memo_id):
    m.delete(memo_id)

def memo_sys(mode : str, user_id : str, receiver_id='', speaker_id='',  message='', memo_id=''):

    if mode == 'DELETE':
        assert memo_id
        delete(memo_id)
        rsp = {'result' : 'successful', 'memo_id' : memo_id}
        return rsp

    elif mode == 'DELETE_ALL':
        assert user_id
        delete_all(user_id=user_id, receiver_id=receiver_id, speaker_id=speaker_id)
        rsp = {'result' : 'successful', 'user_id' : user_id, 'receiver_id' : receiver_id, 'speaker_id' : speaker_id}
        return rsp

    elif mode == 'MEMO':
        assert user_id and receiver_id and speaker_id
        result = add_memory(message=message, user_id=user_id, speaker_id=speaker_id, receiver_id=receiver_id)
        return result

    elif mode == 'SEARCH':
        assert user_id and receiver_id and speaker_id and message
        related_memo = search_memories(message=message, user_id=user_id, receiver_id=receiver_id, speaker_id=speaker_id)
        return related_memo['results']

    elif mode == 'GET_ALL':
        all_memo = get_all_memories(user_id=user_id, receiver_id=receiver_id, speaker_id=speaker_id)
        return all_memo

    else :
        print('data error')
