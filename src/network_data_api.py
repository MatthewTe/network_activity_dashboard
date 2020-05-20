# Importing data management packages:
import pandas as pd
# Importing the Network Data collection packages:
import psutil

# This object inherits directly from the psutil object:
class network_api():
    """
    This method directly inherits the psutil moduel and is only used to
    format the already finished output of the pustil networking package into
    an easily callable/readable format for the network_activity_dashboard.
    """
    def __init__(self):
        '''
        Method builds and creates the instance variables that provide functionality
        for the network_api object.
        '''
        # Declaring an instance variable:
        self.nic_names = network_api.get_nic_names()
        self.nic_main_df = self.build_nic_df()

    def get_nic_counter(nic_name):
        '''
        This method uses the psutil package to return a tuple of data points
        that represent network traffic for the specified network card based on
        the name of the network interface card


        Parameters
        ----------
        nic_name : str
            A string representing the name of the network interface card

        Returns
        -------
        nic_info : tuple
            A tuple of data transmition information at the point of call for the
            specified network interface card using psutl.net_io_counters()
        '''
        # Extracting data from all the network interface cards:
        nic_info_dict = psutil.net_io_counters(pernic=True)

        try:
            # Slicing the network info dict to extract only the data based on the nic name:
            nic_info = nic_info_dict[nic_name]

            return nic_info

        except:
            return None

    def get_nic_stats(nic_name):
        '''
        This method uses the psutil package to return a tuple of data points
        that represent information for the specified network card based on
        the name of the network interface card


        Parameters
        ----------
        nic_name : str
            A string representing the name of the network interface card

        Returns
        -------
        nic_info : tuple
            A tuple of data transmition infnetwork_api().build_nic_df()
            information at the point of call for the
            specified network interface card using psutl.net_if_stats()
        '''
        # Calling the main psutil method that generates the nic info for all NICs:
        nic_info_dict = psutil.net_if_stats()

        # Slicing the nic_info_dict based on input nic_name:
        try:
            nic_info = nic_info_dict[nic_name]
            return nic_info

        except:
            return None

    def get_nic_addrs(nic_name):
        '''
        This method uses the psutil package to return a tuple of data points
        that represent information for the specified network card based on
        the name of the network interface card


        Parameters
        ----------
        nic_name : str
            A string representing the name of the network interface card

        Returns
        -------
        nic_info : tuple
            A tuple of data information at the point of call for the
            specified network interface card using psutl.net_if_addrs()
        '''
        # Calling the main psutil method that generates the nic info for all NICs:
        nic_info_dict = psutil.net_if_addrs()

        # Slicing the nic_info_dict based on input nic_name:
        try:
            nic_info = nic_info_dict[nic_name]
            return nic_info

        except:
            return None

    def get_nic_names():
        '''
        Method returns a list of network card names that are avalible on the
        machine based on the psutil.net_io_counters() method

        Return
        ------
        nic_name_lst : list
            A list of Network Interface Card Names avalible on the device
        '''
        # Creating the nic_name_lst that will be built:
        nic_name_lst = []

        # Calling the NIC dict of named tuples:
        nic_info_dict = psutil.net_io_counters(pernic=True)

        # Itterating through the dict and extracting nic_names:
        for name in nic_info_dict:

            # Adding nic_names to the list:
            nic_name_lst.append(name)


        return nic_name_lst

    def build_nic_df(self):
        '''
        Method makes uses of other network_api methods to build and return a
        pandas dataframe containing current data on each NIC detected on the machine.

        Returns
        -------
        nic_data_df : pandas dataframe
            A dataframe containing all current data on each NIC.
        '''
        # Creating a list of dicts where each dict corresponds to input data row:
        row_dict_lst = []


        # Iterating through each NIC name and creating a row dict:
        for name in self.nic_names:

            # Unpacking tuples generated with network_api methods:
            (isup, duplex, speed, mtu) = network_api.get_nic_stats(name) # psutl.net_if_stats()
            #(family, address, netmask, broadcast, ptp) = network_api.get_nic_addrs(name) # psutl.net_io_counters()

            row_dict = {
                'NIC Name': name,
                'Online Status': isup,
                'Duplex typ': duplex,
                'Speed': speed,
                'Max Unit': mtu,
            }

            row_dict_lst.append(row_dict)

        # Building main dataframe from list of dicts:
        nic_data_df = pd.DataFrame(row_dict_lst)

        return nic_data_df

    def build_net_if_addrs_df(nic_name):
        '''
        Method builds a dataframe out of the list of tuple data produced by the
        psutil.net_if_addrs() method. It slices said data based on the NIC based on
        nic_name

        Parameters
        ----------
        nic_name : str
            The name of the NIC that will be used to slice the data

        Returns
        -------
        nic_address_df : pandas dataframe
            A dataframe containing the addresses associated to the selected NIC.
        '''
        # Creating a list of dicts where each dict is a df row and each dict key
        # is the df column names:
        row_dict_lst = []

        # Declaring the net_if_addrs dict:
        address_data = psutil.net_if_addrs()

        # Slicing dict based on nic_name:
        data_slice = address_data[nic_name]

        # Iterating through the data slice list building the row_dict_lst:
        for tuple in data_slice:

            # Unpacking tuple:
            (family, address, netmask, broadcast, ptp) = tuple

            # Creating a row dict:
            row_dict = {
                'Family Addr': family,
                'Primary Addr': address,
                'Netmask Addr': netmask,
                'Broadcast Addr': broadcast,
                'PtP Addr': ptp
                }

            row_dict_lst.append(row_dict)

        # Building the nic_address_df with list of dicts as data:
        nic_address_df = pd.DataFrame(row_dict_lst)

        return nic_address_df
