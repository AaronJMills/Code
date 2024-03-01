!--------------------------------------------------------------------------!
! The Phantom Smoothed Particle Hydrodynamics code, by Daniel Price et al. !
! Copyright (c) 2007-2023 The Authors (see AUTHORS)                        !
! See LICENCE file for usage and distribution conditions                   !
! http://phantomsph.github.io/                                             !
!--------------------------------------------------------------------------!
module moddump
!
! custom moddump routine: centres the position and velocity coordinates on the selected sink
!
! :References: None
!
! :Owner: Daniel Price
!
! :Runtime parameters: None
!
! :Dependencies: None
!
 implicit none

contains

subroutine modify_dump(npart,npartoftype,massoftype,xyzh,vxyzu)
 use part,      only:xyzmh_ptmass,vxyz_ptmass,nptmass,igas
 integer, intent(inout) :: npart
 integer, intent(inout) :: npartoftype(:)
 integer :: i
 real,    intent(inout) :: massoftype(:)
 real,    intent(inout) :: xyzh(:,:),vxyzu(:,:)

! change all particle coordinates to be relative to second sink
 do i=1,npart
    xyzh(1:3,i) = xyzh(1:3,i) - xyzmh_ptmass(1:3, 2)
    vxyzu(1:3,i) = vxyzu(1:3,i) - vxyz_ptmass(1:3, 2)

 enddo

 do i=1,nptmass
    xyzmh_ptmass(1:3,i) = xyzmh_ptmass(1:3,i) - xyzmh_ptmass(1:3, 2)
    vxyz_ptmass(1:3,i) = vxyz_ptmass(1:3,i) - vxyz_ptmass(1:3, 2)

 enddo

 return
end subroutine modify_dump

end module moddump
