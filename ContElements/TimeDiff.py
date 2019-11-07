#!/usr/bin/env python

#internal imports
from ContElements.Context.PacketDirection import PacketDirection
from ContElements.Context.PacketFlowKey import PacketFlowKey

#For math stuff
import numpy
from scipy import stats as stat

#type hinting imports
from typing import List, Any


#time difference between packets of foward and reverse flows
class TimeDiff:
    """A summary of features based on the time difference between an outgoing packet and the following response.

    Attributes:
        mean_count (int): The number of means
        grand_total (flaot): The cummulation of means


    """

    mean_count = 0
    grand_total = 0

    def __init__(self, feature):
        self.feature = feature

    def get_dif(self) -> List[float]:
        """Gets the time difference in seconds between an outgoing packet and the following response packet.

        Returns:
            List[float]: A list of time differences.

        """
        time_diff = []
        temp_packet = None
        temp_direction = None
        for packet, direction in self.feature.packets:
            if temp_direction == PacketDirection.FORWARD and direction == PacketDirection.REVERSE:
                time_diff.append(packet.time-temp_packet.time)
            temp_packet = packet 
            temp_direction = direction
        return time_diff

    def get_var(self) -> float:
        """Gets the variation of the list of time differences.

        Returns:
            float: The variation in time differences.

        """
        var = -1
        if len(self.get_dif()) != 0:
            var = numpy.var(self.get_dif())
        
        return var

    def get_mean(self) -> float:
        """Gets the mean of the list of time differences.

        Returns:
            float: The mean in time differences.

        """
        mean = -1
        if len(self.get_dif()) != 0:
            mean = numpy.mean(self.get_dif())
        
        return mean

    def _get_grand_total(self) -> float:
        """grand total of time differences in a network flow.

        Returns:
            float: The grand total of time differences in a network flow

        """


        if TimeDiff.mean_count == 0:
            TimeDiff.grand_total = self.get_mean() - self.get_mean()
        else:
            TimeDiff.grand_total += self.get_mean()

        TimeDiff.mean_count += 1

        return TimeDiff.grand_total

    def get_grand_mean(self) -> float:
        """The mean of means of time differences in a network flow.

        Returns:
            float: The grand mean of the time differences

        """

        if (TimeDiff.mean_count > 1):
            TimeDiff.grand_mean = self._get_grand_total()/(TimeDiff.mean_count-1)
        else:
            TimeDiff.grand_mean = self._get_grand_total()/(TimeDiff.mean_count)

        return TimeDiff.grand_mean

    def get_median(self) -> float:
        """Gets the median of the list of time differences

        Returns:
            float: The median in time differences.

        """
        return numpy.median(self.get_dif())

    def get_mode(self) -> float:
        """Gets the mode of the of time differences

        Returns:
            float: The mode in time differences.

        """
        mode = -1
        if len(self.get_dif()) !=0:
            mode = float(stat.mode(self.get_dif())[0])

        return mode
    def get_skew(self) -> float:
        """Gets the skew of the of time differences. 
        Using a simple skew formula using the mean and the median

        Returns:
            float: The skew in time differences.

        """
        mean = self.get_mean()
        median = self.get_median()
        dif = 3*(mean - median)
        std = self.get_std()
        skew = -10
        if std != 0:
            skew = dif/std

        return skew

    def get_skew2(self) -> float:
        """Gets the skew of the of time differences. 
        Using a simple skew formula using the mean and the mode

        Returns:
            float: The skew in time differences.

        """
        mean = self.get_mean()
        mode = self.get_mode()
        dif = (mean - mode)
        std = self.get_std()
        skew2 = -10
        if std !=0:
            skew2 = dif/std

        return skew2

    def get_std(self) -> float:
        """Gets the standard deviation of the list of time differences

        Returns:
            float: The standard deviation in time differences.

        """
        std = -1
        if len(self.get_dif()) != 0:
            std = numpy.sqrt(self.get_var())

        return std

    def get_cov(self) -> float:
        """Gets the coefficient of variance of the list of time differences

        Returns:
            float: The coefficient of variance in time differences.
            return -1 if division by 0.
        """
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std()/self.get_mean()
        
        return cov
        