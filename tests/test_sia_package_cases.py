# from typing import Protocol
from pysiaalarm import (
    InvalidAccountFormatError,
    InvalidAccountLengthError,
    InvalidKeyFormatError,
    InvalidKeyLengthError,
    SIAAccount,
    SIAClient,
    SIAEvent,
    Protocol,
)
from pysiaalarm.sia_errors import EventFormatError
from pysiaalarm.sia_account import SIAResponseType
from tests.test_utils import ACCOUNT, KEY, HOST


class EventParsing:
    """Test cases for event parsing.

    Emits these fields: "line, account_id, type, code, error"

    """

    def case_encrypted(self):
        """Input a encrypted line."""
        return (
            r'60AB0078"*SIA-DCS"5994L0#AAA[5AB718E008C616BF16F6468033A11326B0F7546CAB230910BCA10E4DEBA42283C436E4F8EFF50931070DDE36D5BB5F0C',
            "AAA",
            None,
            None,
            None,
        )

    def case_cl(self):
        """Input a closing report event."""
        return (
            r'E5D50078"SIA-DCS"6002L0#AAA[|Nri1/CL501]_14:12:04,09-25-2019',
            "AAA",
            "Closing Report",
            "CL",
            None,
        )

    def case_op(self):
        """Input a opening report event."""
        return (
            r'90820051"SIA-DCS"4738R0001L0001[#006969|Nri04/OP001NM]',
            "006969",
            "Opening Report",
            "OP",
            None,
        )

    def case_null(self):
        """Input a encrypted null event."""
        return (
            r'76D80055"*NULL"0000R0L0#AAAB[B4BC8B40D0E6D959D6BEA78E88CC0B2155741A3C44FBB96D476A3E557CAD64D9',
            "AAAB",
            None,
            None,
            None,
        )

    def case_wa(self):
        """Input a water alarm event."""
        return (
            r'C4160279"SIA-DCS"5268L0#AAA[Nri1/WA000]_08:40:47,07-08-2020',
            "AAA",
            "Water Alarm",
            "WA",
            None,
        )

    def case_eventformaterror(self):
        """Input a event format error event."""
        return (r"this is not a parsable event", None, None, None, EventFormatError)


class AccountSetup:
    """Test cases for key and account errors.

    Emits these fields: "key, account_id, error"

    """

    def case_InvalidKeyFormat(self):
        """Test invalid key format."""
        return ("ZZZZZZZZZZZZZZZZ", ACCOUNT, InvalidKeyFormatError)

    def case_InvalidKeyLength_15(self):
        """Test invalid key length at 15."""
        return ("158888888888888", ACCOUNT, InvalidKeyLengthError)

    def case_correct_16(self):
        """Test correct key at 16."""
        return ("1688888888888888", ACCOUNT, None)

    def case_InvalidKeyLength_23(self):
        """Test invalid key length at 23."""
        return (
            "23888888888888888888888",
            ACCOUNT,
            InvalidKeyLengthError,
        )

    def case_correct_24(self):
        """Test correct key at 24."""
        return ("248888888888888888888888", ACCOUNT, None)

    def case_InvalidKeyLength_31(self):
        """Test invalid key length at 31."""
        return (
            "3188888888888888888888888888888",
            ACCOUNT,
            InvalidKeyLengthError,
        )

    def case_correct_32(self):
        """Test correct at 32."""
        return ("32888888888888888888888888888888", ACCOUNT, None)

    def case_InvalidAccountLength(self):
        """Test invalid account length at 2."""
        return (KEY, "22", InvalidAccountLengthError)

    def case_InvalidAccountFormat(self):
        """Test invalid account format."""
        return (KEY, "ZZZ", InvalidAccountFormatError)


class TestEncrypted:
    """Test class for encrypted and non-encrypted."""

    def case_encrypted(self):
        return KEY

    def case_unencrypted(self):
        return None


class TestProtocols:
    """Test class for protocols."""

    def case_tcp(self):
        return Protocol.TCP

    def case_udp(self):
        return Protocol.UDP


class TestSyncAsync:
    """Test cases for Async vs Sync."""

    def case_sync(self):
        return True

    def case_async(self):
        return False


class TestFunc:
    """Test cases for failing function or not."""

    def case_good_func(self):
        return False

    def case_bad_func(self):
        return True


class TestConfigs:
    """Test class for client.

    Emits these fields: "config"

    """

    def case_unencrypted_config(self):
        """Test unencrypted config and a good func."""
        return {"host": HOST, "account_id": ACCOUNT, "key": ""}

    def case_encrypted_config(self):
        """Test encrypted config and a good func."""
        return {"host": HOST, "account_id": ACCOUNT, "key": KEY}

class TestMessageType:
    """Test class for Message types."""

    def case_sia(self):
        return "SIA-DCS"

    def case_null(self):
        return "NULL"


class ParseAndCheckEvent:
    """Test cases for parse and check event function.

    Emits these fields: "account_id, code, msg_type, alter_key, wrong_event, response"

    """

    def case_rp(self):
        """Test unencrypted parsing of RP event."""
        return ("RP", False, False, SIAResponseType.ACK)

    def case_wa(self):
        """Test unencrypted parsing of WA event."""
        return ("WA", False, False, SIAResponseType.ACK)

    def case_altered_key(self):
        """Test encrypted parsing of RP event.

        Altered key means the event can be parsed as a SIA Event but the content cannot be decrypted.

        """
        return ("RP", True, False, SIAResponseType.NAK)

    def case_wrong_event(self):
        """Test encrypted parsing of RP event."""
        return ("RP", False, True, SIAResponseType.NAK)
