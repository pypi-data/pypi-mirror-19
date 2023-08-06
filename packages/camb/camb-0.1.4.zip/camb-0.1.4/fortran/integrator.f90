    module ODE_integrator
    USE DVODE_F90_M
    use Precision
    use AMLUtils    
    implicit none

    integer, parameter:: integrator_dverk=1, integrator_vode= 2
    integer :: integrator = integrator_vode

    TYPE (VODE_OPTS) :: OPTS
    external ODE_integrate
    logical ODE_Integrate
    
    !$OMP THREADPRIVATE (OPTS)

    contains


    end module ODE_integrator



    function ODE_integrate(EV,n, fcn, x, y, xend, tol, ind, c, nw, w)result(res)
    use ODE_integrator
    implicit none
    integer n, nw, ind
    logical res
    real(dl) x, y(n), xend, tol, c(*), w(nw,9)
    real EV
    external fcn

    res = .true.
    if (integrator==integrator_dverk) then
        call dverk(EV,n, fcn, x, y, xend, tol, ind, c, nw, w)
        if (ind==-3) res=.false.
    else if (integrator==integrator_vode) then
        if (ind==1) then
            OPTS = SET_NORMAL_OPTS(RELERR=tol, ABSERR=1d-16)
        end if
        call VODE_F90(EV, fcn,n,Y,x,xend,1,ind,OPTS)        
    else
        stop 'unknown integrator'
    end if

    end function ODE_integrate
