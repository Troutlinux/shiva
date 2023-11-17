import os
from glob import iglob

from integrations import virustotal
from integrations import tickercheck
import email_parser


class SHIVAAnalyzer(object):
    def __init__(self, config):
        self._config = config
        self.archive_dir = self._get_archive_path()
        self._parser = email_parser.EmailParser(self._config.QUEUE_DIR)
        self._vt_client = virustotal.VTLookup(config.VT_API_KEY)
        self._tc_client = tickercheck.TCLookup()

    def _get_archive_path(self):
        archive_dir = self._config.ARCHIVE_DIR
        if archive_dir:
            if not os.path.exists(self.archive_dir):
                try:
                    os.mkdir(self.archive_dir)
                except Exception as e:
                    print(f"Failed to create archive dir: {e}")
                    archive_dir = ""
        return archive_dir

    def parse(self, file_key: str) -> dict:
        print(f"Currently parsing {file_key}")
        parsed_info = self._parser.parse(file_key)
        attachments = parsed_info.get("attachments")
        
        # If an attachment is found, then submit the attachment to virustotal. TODO: Store the result.
        #if attachments:
        #    if self._vt_client:
        #        for attachment in attachments:
        #            print(f"Checking {attachment['file_sha256']} hash on VT.")
        #            vt_result = self._vt_client.lookup_file_reputation(attachment['file_sha256'])
        #            if vt_result:
        #                attachment["virustotal"] = vt_result
        
        # Loop over every word in the body of the email
        body = parsed_info.get("body")
        if body:
            if self._tc_client:
                for word in body.split():
                    is_ticker = self._tc_client.validate_if_it_contains_ticker(word)
                    if is_ticker:
                        filename = config.QUEUE_DIR + file_key + '.value'
                        with open(filename, 'w') as f:
                            print(word, file=f)
                            print(file_key, file=f)
                            f.close()
        
        return parsed_info
