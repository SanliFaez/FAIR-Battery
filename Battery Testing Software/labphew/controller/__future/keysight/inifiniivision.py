# -*- coding: utf-8 -*-
"""
    UUTrack.Controller.devices.keysight.inifiniivision.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Driver for the Keysight InfiniiVision DSOX2022A oscilloscope with function generation capabilities.
    
    Source: Programmers Guide, Version 02.39.0000 by Keysight Technologies
    
    .. note:: Not all functions were implemented in the code as methods in the class. However a fair amount of the most
        useful ones was formatted according to Lantz standards.

        IMPORTANT note added 26/7/17
        This version is not tested, Bohdan and Dashka might have newer versions for the keysight oscilloscopes running, check before editing further
    
"""

from lantz import Action
from lantz import Feat, DictFeat
from lantz import Q_
from lantz.messagebased import MessageBasedDriver


class Funcgen(MessageBasedDriver):
    """The agilent 33220a function generator"""
    MANUFACTURER_ID = '0x0957'
    MODEL_CODE = '0x1797'

    DEFAULTS = {'USB': {'write_termination': '\n',
                        'read_termination': '\n',
                        'timeout': 5000,
                        'encoding': 'ascii'
                        }}

    @Action()
    def clear(self):
        return self.write('*CLS')

    @Feat()
    def idn(self):
        return self.query('*IDN?')

    @Feat()
    def serial(self):
        """Returns the serial number of the instrument"""
        self.query(':SER?')

    @Action(limits=(0,9))
    def save(self,value):
        """Stores the current state of the instrument in a save register.
        
        :params int value: of the save register where data will be saved """
        self.write('*SAV %s'%value)

    @Action(limits=(0,10))
    def recall(self,value):
        """Restores the state of the instrument from the specified save/recall register.
        
        :params int value: of the save register from which data will be restored"""
        self.write('*RCL %s'%value)

    @Action()
    def trigger(self):
        """Triggers the device"""
        self.write('*TRG')

    @Feat()
    def self_test(self):
        """Performs a self-test of the instrument. The result of the test is the output. A zero indicates the test
        passed and a non-zero indicates the test failed."""
        return self.query('*TST?')

    @Feat(limits=(1,3))
    def status(self,channel):
        """Reports  whether the channel, function or serial decode bus is displayed.
        :params -- channel"""
        return self.query(':STAT? %s' % channel)



    ### Functions related to the function generator and not to the oscilloscope are prepended
    ### with the word wgen.

    @Feat(units='hertz')
    def wgen_frequency(self):
        """gets the frequency of the function generator
        :params -- frequency (in Hz)
        """
        return self.query(':WGEN:FREQuency?')

    @wgen_frequency.setter
    def wgen_frequency(self,freq):
        self.write(':WGEN:FREQuency %s'%freq)

    @Feat(values={'SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC'})
    def wgen_function(self):
        """Gets the function pased to the function generator"""
        return self.query(':WGEN:FUN?')

    @wgen_function.setter
    def wgen_function(self, fun):
        """Sets the function of the function generator"""
        self.write(':WGEN:FUN %s'%fun)

    @Feat()
    def wgen_pulse_width(self):
        """For Pulse waveforms, the :WGEN:FUNCtion:PULSe:WIDTh specifies the
        width of the pulse.
        The pulse width can be adjusted from 20 ns to the period minus 20 ns."""
        return self.query(':WGEN:FUNCtion:PULSe:WIDTh?')

    @wgen_pulse_width.setter
    def wgen_pulse_width(self,width):
        self.query(':WGEN:FUNCtion:PULSe:WIDTh %s' % width)

    @Feat(limits=(0,100,1))
    def wgen_ramp_symmetry(self):
        """For Ramp waveforms, the :WGEN:FUNCtion:RAMP:SYMMetry command specifies
        the symmetry of the waveform.
        Symmetry represents the amount of time per cycle that the ramp waveform is
        rising."""
        return self.query(':WGEN:FUNCtion:RAMP:SYMMetry?')

    @wgen_ramp_symmetry.setter
    def wgen_ramp_symmetry(self,perc):
        self.write(':WGEN:FUNCtion:RAMP:SYMMetry %i' % perc)

    @Feat(limits=(1,100,1))
    def wgen_square_dcycle(self):
        """Duty cycle is the percentage of the period that the waveform is high."""
        return self.query(':WGEN:FUNCtion:SQUare:DCYCle?')

    @wgen_square_dcycle.setter
    def wgen_square_dcycle(self, perc):
        self.write(':WGEN:FUNCtion:SQUare:DCYCle %i' % perc)

    @Feat(limits=(1,100,1))
    def wgen_amplitude_modulation(self):
        """specifies the amount of amplitude modulation.
        AM Depth refers to the portion of the amplitude range that will be used by the
        modulation. For example, a depth setting of 80% causes the output amplitude to
        vary from 10% to 90% (90% – 10% = 80%) of the original amplitude"""
        return self.query(':WGEN:MODulation:AM:DEPTh?')

    @wgen_amplitude_modulation.setter
    def wgen_amplitude_modulation(self,perc):
        self.write(':WGEN:MODulation:AM:DEPTh %i' % perc)

    @Feat(units='Hz')
    def wgen_amplitude_modulation_frequency(self):
        """specifies the frequency of the modulating signal."""
        return self.query(':WGEN:MODulation:AM:FREQuency?')

    @wgen_amplitude_modulation_frequency.setter
    def wgen_amplitude_modulation_frequency(self, freq):
        self.write(':WGEN:MODulation:AM:FREQuency %s' % freq)

    @Feat(values={'SINusoid', 'SQUare', 'RAMP'})
    def wgen_amplitude_modulation_function(self):
        return self.query(':WGEN:MODulation:FUNCtion?')

    @wgen_amplitude_modulation_function.setter
    def wgen_amplitude_modulation_function(self,func):
        """specifies the shape of the modulating signal."""
        self.write(':WGEN:MODulation:FUNCtion %s' % func)

    @Feat(limits=(1,100,1))
    def wgen_modulation_noise(self):
        """adds noise to the currently selected
        signal. The sum of the amplitude between the original signal and injected noise is
        limited to the regular amplitude limit (for example, 5 Vpp in 1 MOhm), so the range
        for <percent> varies according to current amplitude."""
        return self.query(':WGEN:MODulation:NOISe?')

    @wgen_modulation_noise.setter
    def wgen_modulation_noise(self,perc):
        self.write(':WGEN:MODulation:NOISe %s' % perc)

    @Feat(values={True: 1, False: 0})
    def wgen_modulation(self):
        return self.query(':WGEN:MODulation:STATe?')

    @wgen_modulation.setter
    def wgen_modulation(self,value):
        self.write(':WGEN:MODulation:STATe %s' % value)

    @Feat(values={'AM', 'FM', 'FSK'})
    def wgen_modulation_type(self):
        return self.query(':WGEN:MODulation:TYPE?')

    @wgen_modulation_type.setter
    def wgen_modulation_type(self,modulation):
        self.write(':WGEN:MODulation:TYPE %s' % modulation)

    @Feat(values={True: 1, False: 0})
    def wgen(self):
        """The :WGEN:OUTPut command specifies whether the waveform generator signal
        output is ON (1) or OFF (0)."""
        return self.query(':WGEN:OUTPut?')

    @wgen.setter
    def wgen(self,value):
        self.write(':WGEN:OUTPut' % value)

    @Feat(units='s')
    def wgen_period(self):
        """For all waveforms except Noise and DC, the :WGEN:PERiod command specifies
        the period of the waveform.
        You can also specify the period indirectly using the :WGEN:FREQuency command.
        """
        return self.query(':WGEN:PERiod?')

    @wgen_period.setter
    def wgen_period(self,period):
        self.write(':WGEN:PERiod %s' % period)

    @Action()
    def wgen_reset(self):
        """The :WGEN:RST command restores the waveform generator factory default
        settings (1 kHz sine wave, 500 mVpp, 0 V offset)."""
        self.write(':WGEN:RST')

    @Feat(units='V')
    def wgen_voltage(self):
        """For all waveforms except DC, the :WGEN:VOLTage command specifies the
        waveform's amplitude. Use the :WGEN:VOLTage:OFFSet command to specify the
        offset voltage or DC level."""
        return self.query(':WGEN:VOLTage?')

    @wgen_voltage.setter
    def wgen_voltage(self,volt):
        self.write(':WGEN:VOLTage %s' % volt)

    @Feat(units='V')
    def wgen_voltage_offset(self):
        """The :WGEN:VOLTage:OFFSet command specifies the waveform's offset voltage or
        the DC level. Use the :WGEN:VOLTage command to specify the amplitude."""
        return self.query(':WGEN:VOLTage:OFFSet?')

    @wgen_voltage_offset.setter
    def wgen_voltage_offset(self, volt):
        self.write(':WGEN:VOLTage:OFFSet %s' % volt)




    ### Functions related to the oscilloscope and not to the function generator are prepended
    ### with the word measure.

    @Action(limits=(1, 2))
    def measure_autoscale(self,channel):
        """Autoscale to the defined channel.
        :params -- chanel to use as reference"""
        self.write(':AUT %s'%channel)

    @Feat()
    def measure_digitize(self, channels):
        """It makes the instrument to acquire a waveform according to the settings of the acquire command.
        When the acquisition is complete the instrument is stopped.
        :params -- array of channels to acquire"""
        if type(channels) == type(1):
           s = str(channels)
        elif type(channels) == type([]):
            s = ''
            for c in channels:
                s += '%s,'%c
            s = s[:-1]

        self.write(':DIG %s' % s)

    @Action()
    def measure_run(self):
        """Starts repetitive acquisitions. It is the same as pressing the run key on the front panel."""
        self.write(':RUN')

    @Action()
    def measure_stop(self):
        """stops the acquisition. This is the same as pressing the Stop key on the front panel"""
        self.write(':STOP')

    @Action()
    def measure_single(self):
        """Triggers a single acquisition of data. It is the same as pressing the single button on the control panel."""
        self.write(':SING')

    @Feat(limits=(2,655367))
    def measure_acquire_count(self):
        """In averaging mode, specifies the number of values
        to be averaged for each time bucket before the acquisition is considered to be
        complete for that time bucket. When :ACQuire:TYPE is set to AVERage, the count
        can be set to any value from 2 to 65536."""
        self.query(':ACQ:COUNT?')

    @measure_acquire_count.setter
    def measure_acquire_count(self,count):
        self.write('ACQ:COUNT %s'%count)

    @DictFeat(keys={'RTIM', 'SEGM'})
    def measure_acquire_mode(self):
        """Sets the acquisition mode of the oscilloscope.
        :params -- the mode. RTIM sets the oscilloscope in real time mode; SEGM sets the oscilloscope in segmented
        memory mode"""
        self.query(':ACQ:MODE?')

    @measure_acquire_mode.setter
    def measure_acquire_mode(self,mode):
        self.write(':ACQ:MODE %s' % mode)

    @Feat()
    def measure_points(self):
        """Returns the number of data points that the hardware
        will acquire from the input signal. The number of points acquired is not directly
        controllable."""
        return self.query(':ACQuire:POINts?')

    @Feat()
    def measure_sample_rate(self):
        """Returns the current oscilloscope acquisition sample
        rate. The sample rate is not directly controllable."""
        return self.query(':ACQuire:SRATe?')

    #@DictFeat(keys={'NORMal', 'AVERage', 'HRESolution', 'PEAK'})
    @Feat(values={'NORMal', 'AVERage', 'HRESolution', 'PEAK'})
    def measure_type(self):
        """Selects the type of data acquisition that is to take
        place. The acquisition types are:
        NORMal — sets the oscilloscope in the normal mode.
        AVERage — sets the oscilloscope in the averaging mode. You can set the count
        by using the method measure_acquire_count.
        In this mode, the value for averages is an integer from 1 to 65536. The COUNt
        value determines the number of averages that must be acquired.
        The AVERage type is not available when in segmented memory mode
        • HRESolution — sets the oscilloscope in the high-resolution mode (also known
        as smoothing). This mode is used to reduce noise at slower sweep speeds
        where the digitizer samples faster than needed to fill memory for the displayed
        time range.
        For example, if the digitizer samples at 200 MSa/s, but the effective sample
        rate is 1 MSa/s (because of a slower sweep speed), only 1 out of every 200
        samples needs to be stored. Instead of storing one sample (and throwing others
        away), the 200 samples are averaged together to provide the value for one
        display point. The slower the sweep speed, the greater the number of samples
        that are averaged together for each display point.
        """
        return self.query(':ACQuire:TYPE?')

    @measure_type.setter
    def measure_type(self,mode):
        self.write(':ACQuire:TYPE %s' % mode)

    #@Feat(limits=(1,2))
    def measure_VPP(self, chan):
        """Gets the Voltage peak to peak from the oscilloscope in the desired channel"""
        return self.query(':MEAS:VPP? CHAN%s' % chan) * Q_('volt')

    # @Feat(limits=(1,2))
    def measure_Vmin(self,chan):
        """Measures the minimum voltage from the selected channel. """
        return self.query(':MEAS:VMIN? CHAN%s' % chan) * Q_('volt')

    # @Feat(limits=(1,2))
    def measure_Vmax(self,chan):
        """Measures the maximum voltage from the selected channel. """
        return self.query(':MEAS:VMAX? CHAN%s' % chan) * Q_('volt')

    # @Feat(limits=(1,2))
    def measure_frequency(self,chan):
        """Measures the frequency from the selected channel. """
        return self.query(':MEAS:FREQ? CHAN%s' % chan) * Q_('hertz')

    @Action()
    def measure_clear(self):
        """Clears all the measurements from the screen."""
        self.write(':MEASure:CLEar')
        return True

    @Feat()
    def measure_waveform(self):
        """Returns the binary block of sampled data points
        transmitted using the IEEE 488.2 arbitrary block data format. The binary data is
        formatted according to the settings of the :WAVeform:UNSigned,
        :WAVeform:BYTeorder, :WAVeform:FORMat, and :WAVeform:SOURce commands.
        The number of points returned is controlled by the :WAVeform:POINts command"""
        return self.query(':WAVeform:DATA?')

    @Feat(values={'WORD', 'BYTE', 'ASCii'})
    def measure_format(self):
        """Sets the data transmission mode for waveform
        data points. This command controls how the data is formatted when sent from the
        oscilloscope.
        • ASCii formatted data converts the internal integer data values to real Y-axis
        values. Values are transferred as ASCii digits in floating point notation,
        separated by commas.
        ASCII formatted data is transferred ASCii text.
        • WORD formatted data transfers 16-bit data as two bytes. The
        :WAVeform:BYTeorder command can be used to specify whether the upper or
        lower byte is transmitted first. The default (no command sent) is that the upper
        byte transmitted first.
        • BYTE formatted data is transferred as 8-bit bytes."""
        self.query(':WAVeform:FORMat?')

    @measure_format.setter
    def measure_format(self,f):
        self.write(':WAVeform:FORMat %s' % f)

    @Feat()
    def measure_points(self):
        """sets the number of waveform points to be
        transferred with the measure_waveform command. This value represents the points
        contained in the waveform selected with the :WAVeform:SOURce command.
        For the analog or digital sources, the records that can be transferred depend on
        the waveform points mode. The maximum number of points returned for math
        (function) waveforms is determined by the NORMal waveform points mode.
        """
        return self.query(':WAVeform:POINts?')

    @measure_points.setter
    def measure_points(self,points):
        self.write(':WAVeform:POINts %s'%points)

    @Feat(values={'NORMal', 'MAXimum', 'RAW'})
    def measure_points_mode(self):
        """Sets the data record to be transferred.
        For the analog or digital sources, there are two different records that can be
        transferred:
        • The first is the raw acquisition record. The maximum number of points available
        in this record is returned by the :ACQuire:POINts? query. The raw acquisition
        record can only be transferred when the oscilloscope is not running and can
        only be retrieved from the analog or digital sources.
        • The second is referred to as the measurement record and is a 62,500-point
        (maximum) representation of the raw acquisition record. The measurement
        record can be retrieved from any source.
        If the <points_mode> is NORMal the measurement record is retrieved.
        If the <points_mode> is RAW, the raw acquisition record is used. Under some
        conditions, such as when the oscilloscope is running, this data record is
        unavailable.
        If the <points_mode> is MAXimum, whichever record contains the maximum
        amount of points is used. Usually, this is the raw acquisition record. But, if the raw
        acquisition record is unavailable (for example, when the oscilloscope is running),
        the measurement record may have more data. If data is being retrieved as the
        oscilloscope is stopped and as the data displayed is changing, the data being
        retrieved can switch between the measurement and raw acquisition records.
        """
        return self.query(':WAVeform:POINts:MODE?')

    @measure_points_mode.setter
    def measure_points_mode(self,mode):
        self.write(':WAVeform:POINts:MODE %s'%mode)

    @Feat()
    def measure_waveform_preamble(self):
        """requests the preamble information for the
        selected waveform source. The preamble data contains information concerning
        the vertical and horizontal scaling of the data of the corresponding channel.
        <format 16-bit NR1>,
        <type 16-bit NR1>,
        <points 32-bit NR1>,
        <count 32-bit NR1>,
        <xincrement 64-bit floating point NR3>,
        <xorigin 64-bit floating point NR3>,
        <xreference 32-bit NR1>,
        <yincrement 32-bit floating point NR3>,
        <yorigin 32-bit floating point NR3>,
        <yreference 32-bit NR1>
        """
        return self.query(':WAVeform:PREamble?')

    @Feat(limits=(1, 2))
    def measure_waveform_source(self):
        """selects the analog channel, function, digital
        pod, digital bus, reference waveform, or serial decode bus to be used as the source.
        IMPORTANT: Currently only implemented for channel 1 or 2."""
        return self.query(':WAVeform:SOURce?')

    @measure_waveform_source.setter
    def measure_waveform_source(self,source):
        self.write(':WAVeform:SOURce CHAN%s' % source)



if __name__ == '__main__':
    with Funcgen.via_usb() as inst:
        inst.initialize()

        print(inst.idn)
        inst.measure_run()
        print('++++++++++++++++++++')
        print("VPP in channel 1: %s" % inst.measure_VPP(1))
        print("VMax in channel 1: %s" % inst.measure_Vmax(1))
        print("VMin in channel 1: %s" % inst.measure_Vmin(1))
        print("Freq in channel 1: %s" % inst.measure_frequency(1))
        print("Sample rate: %s" % inst.measure_sample_rate)
        print('++++++++++++++++++++')
        inst.measure_points = 100
        print("Preamble:")
        print(inst.measure_waveform_preamble)
        inst.measure_waveform_source = 1
        print("Data from %s" % inst.measure_waveform_source)
        inst.measure_format = 'ASCii'
        print(inst.measure_waveform)
        inst.measure_waveform_source = 2
        print("Data from %s" % inst.measure_waveform_source)
        print(inst.measure_waveform)
        inst.measure_type = 'AVERage'
        inst.measure_acquire_count = 10