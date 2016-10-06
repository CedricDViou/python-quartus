# generate the new files needed by quartus for compilation
from os import getenv
from os.path import expanduser, join
from sys import platform


class Setup(object):
    """
    Set up path variables for compilation
    """
    @property
    def altera_path(self):
        # makefile to compile, convert, and upload an altera FPGA image to a jtag
        # device memory.
        if platform == "linux" or platform == "linux2":
            return expanduser("~/altera_lite/15.1/quartus/bin")
        else:
            return "C:\\altera_lite\\15.1\quartus\\bin64"
    @property
    def run_shell(self):
        if platform == "linux" or platform == "linux2":
            return False
        else:
            # windows requires running as shell
            return True

    @property
    def tmp_folder(self):
        if platform == "linux" or platform == "linux2":
            return '/tmp'
        else:
            return join(getenv('USERPROFILE'), 'AppData\Local\Temp')


def conversion_file(output_jic_filename, sof_filename, eeprom='EPCS64',
                      flash_device='EP4CE22'):
    """
    Create the conversion file between the eeprom .sof file and the flash
    memory device jic.
    :param output_jic_filename: The target output filename
    :type output_jic_filename: str
    :param sof_filename: The compiled SRAM object file.
    :type sof_filename: str
    :param eeprom: The name of the eeprom chip.
    :type eeprom: str
    :param flash_device: The name of flash chip.
    :type flash_device: str
    :return: The filename of the conversion file.
    :rtype: str
    """
    setup = Setup()
    output = '<?xml version="1.0" encoding="US-ASCII" standalone="yes"?>\n' \
             '<cof>\n' \
             '  <eprom_name>'+eeprom+'</eprom_name>\n' \
             '  <flash_loader_device>'+flash_device+'</flash_loader_device>\n' \
             '	<output_filename>'+output_jic_filename+'</output_filename>\n' \
             '	<n_pages>1</n_pages>\n' \
             '	<width>1</width>\n' \
             '	<mode>7</mode>\n' \
             '	<sof_data>\n' \
             '		<user_name>Page_0</user_name>\n' \
             '		<page_flags>1</page_flags>\n' \
             '		<bit0>\n' \
             '			<sof_filename>'+sof_filename+'</sof_filename>\n' \
             '		</bit0>\n' \
             '	</sof_data>\n' \
             '	<version>9</version>\n' \
             '	<create_cvp_file>0</create_cvp_file>\n' \
             '	<create_hps_iocsr>0</create_hps_iocsr>\n' \
             '	<auto_create_rpd>0</auto_create_rpd>\n' \
             '	<create_fif_file>0</create_fif_file>\n' \
             '	<options>\n' \
             '		<map_file>1</map_file>\n' \
             '	</options>\n' \
             '	<advanced_options>\n' \
             '		<ignore_epcs_id_check>2</ignore_epcs_id_check>\n' \
             '		<ignore_condone_check>2</ignore_condone_check>\n' \
             '		<plc_adjustment>0</plc_adjustment>\n' \
             '		<post_chain_bitstream_pad_bytes>-1' \
             '</post_chain_bitstream_pad_bytes>\n' \
             '		<post_device_bitstream_pad_bytes>-1' \
             '</post_device_bitstream_pad_bytes>\n' \
             '		<bitslice_pre_padding>1</bitslice_pre_padding>\n' \
             '	</advanced_options>\n' \
             '</cof>\n'
    filename = join(setup.tmp_folder, 'conversion_setup.cof')
    if isfile(filename):
        remove(filename)
    try:
        _file = open(filename, 'w+')
        _file.write(output)
        _file.close()
    except IOError as e:
        print("cannot identify: |", getenv('USERPROFILE'), "|", setup.tmp_folder)
    return filename


def target_file(db_foldername, eeprom='EPCS64', flash_device='EP4CE22'):
    setup = Setup()
    output = 'JedecChain;\n' \
             '	FileRevision(JESD32A);\n' \
             '	DefaultMfr(6E);\n' \
             '	P ActionCode(Cfg)\n' \
             '		Device PartName('+flash_device+')' \
             'Path(\"'+db_foldername+'\")' \
             'File(\"output_file.jic\") MfrSpec' \
             '		(OpMask(1) SEC_Device('+eeprom+') Child_OpMask(1 ' \
             '7));\n' \
             'ChainEnd;\n' \
             'AlteraBegin;\n' \
             '	ChainType(JTAG);\n' \
             'AlteraEnd;\n'
    filename = join(setup.tmp_folder, 'target_memory.cdf')
    if isfile(filename):
        remove(filename)
    _file = open(filename, 'w+')
    _file.write(output)
    _file.close()
    return filename
