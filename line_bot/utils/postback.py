import itertools

from enum import Enum
from functools import reduce
from dataclasses import dataclass
from typing import Any, Callable, Union


class QuestionPostback:
    

    class QuestionModeType:
        TEST = 0
        REVISE = 1


    class PostbackFlag:
        SELECT_CATEGORY = 0
        SELECT_SUBJECT = 1
        SELECT_MODE = 2
        QUESTION = 3
        QUESTION_REVIEW = 4


    class ReplyAnswer:
        # chr_range  = range(int("4E00", 16), int("9FFF", 16))  # 20,992 character
        # encode_map = {"".join(k): chr(v) for k, v in zip(itertools.product("ABCDE*-", repeat=5), chr_range)}
        # decode_map = {chr(k): "".join(v) for k, v in zip(chr_range, itertools.product("ABCDE*-", repeat=5))}

        # @staticmethod
        # def encode(string: str) -> str:
        #     result = ""
        #     for i in range(0, len(string), 5):
        #         s = string[i: 5+i]
        #         if len(s) < 5:
        #             s += "-" * ((5 - len(string)) % 5)
        #         try:
        #             result += QuestionPostback.ReplyAnswer.encode_map[s]
        #         except KeyError:
        #             raise ValueError(f"Invalid segment: {s}")
        #     return result

        # @staticmethod
        # def decode(string: str) -> str:
        #     result = ""
        #     for s in string:
        #         try:
        #             result += QuestionPostback.ReplyAnswer.decode_map[s]
        #         except KeyError:
        #             raise ValueError(f"Invalid character: {s}")
        #     return result.replace("-", "")

        @staticmethod
        def encode(string: str) -> str:
            result = []
            string = reduce(lambda s, kv: s.replace(*kv), dict(zip("ABCD*", "12345")).items(), string)
            for s in range(0, len(string), 4):
                result.append(chr(int(string[s:s+4].ljust(4, "0"), 16)))
            return "".join(result)

        @staticmethod
        def decode(string: str) -> str:
            result = []
            for s in string:
                result.append(hex(ord(s)).removeprefix("0x").replace("0", ""))
            result = reduce(lambda s, kv: s.replace(*kv), dict(zip("12345", "ABCD*")).items(), "".join(result).upper())
            return result
        
        @staticmethod
        def count_correct_answers(string: str, decode: bool = False) -> int:
            if decode:
                result = QuestionPostback.ReplyAnswer.decode(string)
            else:
                result = string
            return result.count("*")
        
        @staticmethod
        def count_incorrect_answers(string: str, decode: bool = False) -> int:
            if decode:
                result = QuestionPostback.ReplyAnswer.decode(string)
            else:
                result = string
            return len(result) - result.count("*")

    @dataclass
    class PostbackField:
        field_size: Union[int, range]
        default: Any
        decoder: Callable
        encoder: Callable

    # Line postback 300 字數限制
    meta = {
        "flag"           : PostbackField(field_size=1, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:01x}".format(s)),
        "category_id"    : PostbackField(field_size=4, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:04x}".format(s)),
        "subject_id"     : PostbackField(field_size=4, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:04x}".format(s)),
        "question_index" : PostbackField(field_size=4, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:04x}".format(s)),
        "mode"           : PostbackField(field_size=1, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:01x}".format(s)),
        "question_seed"  : PostbackField(field_size=4, default=0, decoder=lambda x: int(x, 16), encoder=lambda s: "{:04x}".format(s)),
        "reply_answer"   : PostbackField(field_size=range(0, 282), default="", decoder=ReplyAnswer.decode, encoder=ReplyAnswer.encode),
    }

    def __init__(self, user_profile: str, row_string: str):
        meta = QuestionPostback.meta

        self.user_profile = user_profile
        self.row_string = row_string

        pos = 0
        for k, v in meta.items():
            field_size = v.field_size.stop if isinstance(v.field_size, range) else v.field_size
            value = v.decoder(row_string[pos:pos+field_size])
            setattr(self, k, value)
            pos += field_size
    
    def configure(self, **kwargs) -> str:
        meta = QuestionPostback.meta
        result = ""

        for k, v in meta.items():
            encoder = v.encoder
            value = encoder(kwargs.get(k, getattr(self, k)))
            
            if isinstance(v.field_size, int):
                if len(value) != v.field_size:
                    raise ValueError(f"Encoded value length mismatch for {k}: {value}")
            elif isinstance(v.field_size, range):
                if len(value) not in v.field_size:
                    raise ValueError(f"Encoded value length out of range for {k}: {value}")
            
            result += value

        return result
    
    @staticmethod
    def initialize(**init_kwargs) -> str:
        meta = QuestionPostback.meta
        result = ""

        for k, v in meta.items():
            encoder = v.encoder
            default_value = init_kwargs.get(k, v.default)
            encoded_value = encoder(default_value)

            if isinstance(v.field_size, int):
                if len(encoded_value) != v.field_size:
                    raise ValueError(f"Encoded value length mismatch for {k}: {encoded_value}")
            elif isinstance(v.field_size, range):
                if len(encoded_value) not in v.field_size:
                    raise ValueError(f"Encoded value length out of range for {k}: {encoded_value}")
            
            result += encoded_value

        return result