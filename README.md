# myblog

我的blog项目，地址[在这里](http://39.108.239.113/)

功能正在完善，但是基本的app逻辑，数据库表单已经完善，对大型网站的建设有实践意义。下面我来分享一下我这次实践中对web开发的一点理解。

## 整体概述

个人博客实际上只相当于网站结构上的一个app，而真正的网站肯定需要不止一个app，但是总体流程是不会变的：

- 根据具体app的逻辑编写[模型 models 文件](https://github.com/fudonglai/myblog/blob/master/blog/models.py)，model指的是**数据关系**模型，也就是设计数据库。例如我的这个博客的数据库模型[在这里](https://github.com/fudonglai/info_sys_python/blob/master/Django_code_comments/db.sqlite3)，其中的SQL代码是python自动生成的，但是数据库逻辑和优化必须要专门人员来做。 我的blog项目里面其实包含了两个 app，一个是文章相关的信息（标题，作者，内容，发布时间等等），一个是评论相关信息，Django 建议将评论和文章分开，两个关系只需要一个外键连接就好了。最主要的是文章信息，其中包含一对多的 ForeignKey 关系（Category对Post，Author对Post），多对多关系（Tag和Post），需要明确的是一对多关系的删除异常问题，我就忽略这个问题，导致删除某个 Category 导致所有文章删除。

- **视图逻辑**编写，即[ views 文件和 urls映射 ](https://github.com/fudonglai/myblog/tree/master/blog)。比如你可以观察我的博客中不同功能区的url特点，不同功能区需要明确的url区分，然后对应到[templates](https://github.com/fudonglai/myblog/tree/master/blog/templates)中相应的HTML文件显示视图。
  
- 前端需要制作css样式和js渲染，这个我就不了解了，我的css和js是网上下载的模板，只要和HTML匹配就行。HTML文件要**便于后端改造**成[Django渲染模板](https://github.com/fudonglai/myblog/tree/master/blog/templates)(注意html中有很多{%  %} {{  }}这样的标记，这就是Django的HTML上下文映射)。

  
