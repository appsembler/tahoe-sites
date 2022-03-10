


class IsSuperuserOrStaffPermission:
    def has_permission(self, request, view):
        return is_active_staff_or_superuser(request)


class IsSiteAdminPermission:
    def has_permission(self, request, view):
        site = get_requested_site(request)
        return is_site_admin(site, request.user)
