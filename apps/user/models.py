from django.db import models
from django.contrib.auth.models import AbstractUser


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=30, unique=True, verbose_name="权限名")
    url = models.CharField(verbose_name='含正则的URL', null=True, blank=True, max_length=128)

    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='ps', null=True, blank=True,
                            help_text="对于无法作为菜单的URL，可以为其选择一个可以作为菜单的权限，那么访问时，则默认选中此权限",
                            limit_choices_to={'menu__isnull': False}, on_delete=models.SET_NULL)
    # 让权限去挂靠到菜单下面，而权限表里有菜单的层级关系，权限表也可作为菜单
    menu = models.ForeignKey(verbose_name='菜单', to='Menu', on_delete=models.SET_NULL, null=True, blank=True, help_text='null表示非菜单')

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Role(models.Model):
    """
     角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)
    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class User(AbstractUser):
    """
    用户：划分角色
    """
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    department = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    # 多对多，一个人有多个角色，多个人同属于一个角色
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.username


class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门")
    )
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=organization_type_choices, default="company", verbose_name="类型")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类组织")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
