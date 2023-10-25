from __future__ import annotations
from typing import Optional, Iterable, Iterator, cast
from functools import reduce

fixdict = {}
fixdict["start"] = "8"
fixdict["body_len"] = "9"
fixdict["checksum"] = "10"
fixdict["msg_type"] = "35"

exceptions = ["8", "9", "10"]


def compose_message(fix_dictionary, fix_exceptions, **kwargs):
    msg = ""
    for arg in kwargs:
        if fix_dictionary[arg] not in fix_exceptions:
            msg += fix_dictionary[arg] + "=" + kwargs[arg] + "\001"
    msg = fix_dictionary["body_len"] + "=" + str(len(msg)) + msg
    msg = fix_dictionary["start"] + "=" + "FIX.4.4" + msg

    checksum = reduce(lambda x, y: x + y, list(map(ord, msg))) % 256
    msg += fix_dictionary["checksum"] + "=" + str(checksum)
    return msg


class FIX_State:
    def enter(self, message: "Message") -> "FIX_State":
        return self

    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        return self

    def valid(self, message: "Message") -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Waiting(FIX_State):
    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        if input == ord(b"8"):
            return HEADER
        return self


class Header(FIX_State):
    def enter(self, message: "Message") -> "FIX_State":
        message.reset()
        return self

    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        if input == ord(b"8"):
            return HEADER
        size = message.body_append(input)
        if input == ord(b"9"):
            return BODY
        return self


class Body(FIX_State):
    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        if input == ord(b"8"):
            return HEADER
        size = message.body_append(input)
        if size == 16:
            message.checksum_computed += 1
            return CHECKSUM
        return self


class Checksum(FIX_State):
    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        if input == ord(b"8"):
            return HEADER
        if input in {ord(b"\n"), ord(b"\r")}:
            return END
        size = message.checksum_append(input)
        if size == 6:
            return END
        return self


class End(FIX_State):
    def feed_byte(self, message: "Message", input: int) -> "FIX_State":
        if input == ord(b"8"):
            return HEADER
        if input not in {ord(b"\n"), ord(b"\r")}:
            return WAITING
        return self

    def valid(self, message: "Message") -> bool:
        return message.valid


WAITING = Waiting()
HEADER = Header()
BODY = Body()
CHECKSUM = Checksum()
END = End()


class Message:
    def __init__(self) -> None:
        self.body = bytearray(80)
        self.checksum_source = bytearray(6)
        self.body[0] = ord("8")
        self.body_len = 1
        self.checksum_len = 0
        self.checksum_computed = 0
        self.checksum_computed += ord("8")
        self.checksum_computed %= 256

    def reset(self) -> None:
        self.body[0] = ord("8")
        self.body_len = 1
        self.checksum_len = 0
        self.checksum_computed = 0
        self.checksum_computed += ord("8")
        self.checksum_computed %= 256

    def body_append(self, input: int) -> int:
        self.body[self.body_len] = input
        self.body_len += 1
        self.checksum_computed += input
        self.checksum_computed %= 256
        return self.body_len

    def checksum_append(self, input: int) -> int:
        self.checksum_source[self.checksum_len] = input
        self.checksum_len += 1
        return self.checksum_len

    @property
    def valid(self) -> bool:
        return (
            self.checksum_len == 6
            and int(self.checksum_source[3:]) == self.checksum_computed
        )

    def header(self) -> bytes:
        return bytes(self.body[2:9])

    def body_len_number(self) -> bytes:
        return bytes(self.body[11:12])

    def message_type(self) -> list[bytes]:
        return bytes(self.body[15:16])

    def __repr__(self) -> str:
        body = self.body[: self.body_len]
        checksum = self.checksum_source[: self.checksum_len]
        return f"Message({body}, {checksum}, computed={self.checksum_computed:02x})"

    def message(self) -> bytes:
        return (
            b"8="
            + bytes(self.header())
            + b"9="
            + bytes(self.body_len_number())
            + b"35="
            + bytes(self.message_type())
            + bytes(self.checksum_source)
        )


class Reader:
    def __init__(self) -> None:
        self.buffer = Message()
        self.state: FIX_State = WAITING

    def read(self, source: Iterable[bytes]) -> Iterator[Message]:
        for byte in source:
            new_state = self.state.feed_byte(self.buffer, cast(int, byte))
            if self.buffer.valid:
                yield self.buffer
                self.buffer = Message()
                new_state = WAITING
            if new_state != self.state:
                new_state.enter(self.buffer)
                self.state = new_state


message = b"""
8=FIX.4.49=535=510=166
"""
rdr = Reader()
result = list(rdr.read(message))
print(result[0].message())


# message = compose_message(fixdict, exceptions, msg_type="5")
# # # 8=FIX.4.49=535=510=166
# print(message)
