module netcdfmod
! Module to read from and write to netCDF files
!
! This module contains the necessary types and subroutines to handle netCDF
! files

type variable_3d
    character(50) :: name
    character(50) :: dims(3)
    character(50) :: long_name
    character(50) :: units = ''
    character(50) :: standard_name = ''
    real, allocatable :: data(:, :, :)

end type variable_3d



end module netcdfmod