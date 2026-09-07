import random


class Name:
    def __init__(self, name: str, aliases: list[str] | None = None, prefered_name:str | None = None):
        self._name = name
        self._aliases = aliases if aliases else []
        self._prefered_name = None
        self.prefered_name = prefered_name
        self._id = "{}-{}".format(
            self.name,
            "".join([str(random.choice(list(range(10)))) for x in range(10)]),
        )

    def who_am_I(self):
        result = []

        if self._aliases:
            result += self._aliases
        if self._name and self._name not in result:
            result.append(self._name)
        if self._prefered_name and self.prefered_name not in result:
            result.append(self.prefered_name)
        if self._id and self._id not in result:
            result.append(self.id)
        return result

    def am_I(self, value: str) ->  bool:
        return value in self.who_am_I()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self._prefered_name:
            return self._prefered_name
        return self._name

    @property
    def prefered_name(self):
        return self._prefered_name

    @prefered_name.setter
    def prefered_name(self, value):
        if value not in self._aliases:
            self._aliases.append(value)
        self._prefered_name = value
    