from modules import Module

class Main(Module):

  def __init__(self):
    super().__init__(
      index=0,
      name="sample",
      title="Overview Sample",
      icon="fa fa-connectdevelop",
      path=f"{str(__name__).replace('.', '/')}"
    )

  def handle_request(self, **kwargs):
    return {
      "data_rows": [
        {
          "name" : "foo",
          "project" : "project-foo",
          "source" : "https://github.com/project-foo/foo",
          "health" : "healthy"
        },
        {
          "name": "bar",
          "project": "project-bar",
          "source": "https://github.com/project-bar/bar",
          "health": "healthy"
        },
        {
          "name": "baz",
          "project": "project-baz",
          "source": "https://github.com/project-baz/baz",
          "health": "healthy"
        }
      ]
    }
