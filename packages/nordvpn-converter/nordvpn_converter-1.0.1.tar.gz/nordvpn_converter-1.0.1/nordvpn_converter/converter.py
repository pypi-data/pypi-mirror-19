# -*- coding: utf-8 -*-
import os
import os.path
import uuid
import getpass

NM_TEMPLATE = "data/nm_template"

# CONFIGURATION PLACEHOLDERS
# spaces are intentionally let by the end of the word
CIPHER = 'cipher '
TA_DIRECTION = 'key-direction '
REMOTE_IP = 'remote '


# TEMPLATE PLACEHOLDERS
T_CIPHER = '{{ CIPHER }}'
T_TA_DIRECTION = '{{ TA_DIRECTION }}'
T_REMOTE_IP = '{{ REMOTE_IP }}'
T_VPN_USERNAME = '{{ VPN_USERNAME }}'
T_USERNAME = '{{ USERNAME }}'
T_NAME = '{{ NAME }}'
T_CA_CRT = '{{ CA_CRT }}'
T_TLS_KEY = '{{ TLS_KEY }}'
T_UUID = '{{ UUID }}'


class Converter(object):
    _source_folder = None        #: OpenVPN configuration folder
    _destination_folder = None   #: Output folder
    _certs_folder = None         #: OpenVPN Certificates configuration folder
    _username = None             #: NordVPN username

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self._extracted_data = {}

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._template = os.path.join(dir_path, NM_TEMPLATE)

    def do_conversion(self):
        """The workhorse here"""
        self.pprint("Starting conversion...", appmsg=True)

        for f in os.listdir(self._source_folder):
            if f.endswith('.ovpn'):
                self.pprint("{:>10s} Processing file {}".format(' ', f))
                extracted_info = self.extract_information(f)
                self.output_template(extracted_info)

        self.pprint("Conversion ended. Check the destination folder.", appmsg=True)

    def set_source_folder(self, source_input):
        """Sets the source folder for the openvpn config files"""
        if not source_input or not os.path.isdir(source_input):
            raise Exception("You have to specify a valid path for the source configuration folder.")

        self._source_folder = source_input

    def set_destination_folder(self, source_input):
        """
        Sets the destination folder for the output
        It tries to create the folder if it doesn't exist
        """
        try:
            os.makedirs(source_input, exist_ok=True)
        except Exception:
            raise Exception("You have to specify a valid path for the destination folder.")

        self._destination_folder = source_input

    def set_certs_folder(self, certs_input):
        """Sets the certificates source folder"""
        if not certs_input or not os.path.isdir(certs_input):
            raise Exception("You have to specify a valid path for the certificates source folder.")

        self._certs_folder = certs_input

    def set_username(self, name):
        """Username for the VPN connection"""
        if not name:
            raise Exception("You have to specify an username.")

        self._username = name

    def extract_information(self, input_file):
        """Extracts the needed information from the source configuration files"""
        self.pprint("--> {:>10s} Starting to extract information for {}".format(' ', input_file))

        input_file_full = os.path.join(self._source_folder, input_file)
        with open(input_file_full) as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("#"): continue
            self._extract_cipher(line)
            self._extract_ta_direction(line)
            self._extract_remote_ip(line)

        self._extract_vpn_name(input_file)
        self._extract_vpn_username()
        self._extract_uuid()
        self._extract_username()
        self._extract_certificates(input_file)

        return self._extracted_data

    def output_template(self, extracted_data):
        """Builds the output file based on the extracted data"""
        with open(self._template) as template:
            content = template.read()
            content = content \
                .replace(T_NAME, extracted_data[T_NAME]) \
                .replace(T_UUID, str(extracted_data[T_UUID])) \
                .replace(T_USERNAME, extracted_data[T_USERNAME]) \
                .replace(T_TA_DIRECTION, str(extracted_data[T_TA_DIRECTION])) \
                .replace(T_REMOTE_IP, extracted_data[T_REMOTE_IP]) \
                .replace(T_CIPHER, extracted_data[T_CIPHER]) \
                .replace(T_VPN_USERNAME, extracted_data[T_VPN_USERNAME]) \
                .replace(T_CA_CRT, extracted_data[T_CA_CRT]) \
                .replace(T_TLS_KEY, extracted_data[T_TLS_KEY])

            output_filename = "{}_nordvpn_com".format(extracted_data[T_NAME].replace(".", "_"))
            output_file = os.path.join(self._destination_folder, output_filename)
            with open(output_file, "wt") as output:
                output.write(content)

            self.pprint("<-- {:>10s} Output to file {}".format(' ', output_file))

    def _extract_cipher(self, line):
        """Specific extractor for the cipher"""
        if CIPHER in line:
            _, value = line.split()
            self._extracted_data[T_CIPHER] = value

    def _extract_ta_direction(self, line):
        """Specific extractor for the TA Direction"""
        if TA_DIRECTION in line:
            _, value = line.split()
            self._extracted_data[T_TA_DIRECTION] = int(value)

    def _extract_remote_ip(self, line):
        """Specific extractor for the remote IP"""
        if REMOTE_IP in line:
            _, value, _ = line.split()
            self._extracted_data[T_REMOTE_IP] = value

    def _extract_vpn_name(self, input_file):
        """
        Specific extractor for VPN configuration name
        e.g. us99.nordvpn.com.udp1194.ovpn
        """
        vpn_name = input_file.__str__()
        vpn_name = vpn_name.replace('nordvpn.com.', '').replace('.ovpn', '')

        self._extracted_data[T_NAME] = vpn_name

    def _extract_uuid(self):
        """More like a generator not an extractor"""
        self._extracted_data[T_UUID] = uuid.uuid4()

    def _extract_vpn_username(self):
        """Username for the VPN connection"""
        self._extracted_data[T_VPN_USERNAME] = self._username

    def _extract_username(self):
        """Local system username; for now the current running user"""
        self._extracted_data[T_USERNAME] = getpass.getuser()

    def _extract_certificates(self, input_file):
        """
        Sets up certificates
        Fixed format: us99_nordvpn_com_ca.crt / us99_nordvpn_com_tls.key for a file as us99.nordvpn.com.udp1194.ovpn
        """
        raw_name = input_file.__str__()
        raw_split = raw_name.split(".")[:3]

        cert_name = "{}.crt".format("_".join(raw_split + ['ca']))
        tls_name = "{}.key".format("_".join(raw_split + ['tls']))

        self._extracted_data[T_CA_CRT] = os.path.join(self._certs_folder, cert_name)
        self._extracted_data[T_TLS_KEY] = os.path.join(self._certs_folder, tls_name)

    def pprint(self, msg, appmsg=False):
        """
        Generic function to conditionally print messages
        application messages are always printed out
        debug messages are printed out based on the value of debugMode flag
        """
        if appmsg:
            print(msg)
            return

        if self.debug_mode:
            print(msg)
