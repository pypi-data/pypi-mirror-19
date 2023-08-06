"""Support for the UserData resource in Skytap.

Specifically, this is for custom ('user data') that's applied to an environment
or VM. This data can be text or, in the context of using it with this Skytap
script, it can also be JSON or YAML and will then be re-parsed.

This allows users to put data into a VM user data block and it'll filter down
and be accessible to this script. We use this to expose variables to the user
like shutdown time and other automation pieces.
"""
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource


class UserData(SkytapResource):
    """UserData object to handle custom user data for a Skytap object.

    This typically would be for a VM or Environment.
    """

    def __init__(self, contents, env_url):
        """Create the UserData object."""
        super(UserData, self).__init__(contents)
        self.url = env_url + '/user_data.json'

    def __str__(self):
        """Express the userdata as a string."""
        return self.contents

    def add(self, key, value):
        """Add value to environment's userdata.

        Args:
            key (str): The name of the value's key.
            value (str): The value to add.

        Returns:
            str: The response from Skytap, or "{}".
        """
        add_key = True

        lines = self.contents.split("\n")

        for i in lines:
            if i != "":
                j = i.split()
                if len(j) > 0 and j[0] == (key + ":"):
                    add_key = False

        if add_key:
            Utils.info('Adding key \"' + key + '\" with value \"'
                       '' + value + '\"')
            api = ApiClient()
            new_content = "" + key + ": " + value + "\n" + self.contents
            data = {"contents": new_content}
            response = api.rest(self.url, data, 'POST')
            self.data[key] = value
            self.refresh()
            return response
        else:
            Utils.info('Key \"' + key + '\" with value \"' + value + '\"'
                       'already exists.')
            return "{}"

    def delete(self, key):
        """Delete key/value from environment's userdata.

        Args:
            key (str): The name of key to delete, along with value

        Returns:
            str: The response from Skytap, or "{}".
        """
        new_content = ""

        del_key = False

        lines = self.contents.split("\n")

        for i in lines:
            if i != "":
                j = i.split()
                if len(j) > 0 and j[0] == (key + ":"):
                    del_key = True
                else:
                    new_content += (i.strip() + "\n")

        if del_key:
            Utils.info('Deleting key \"' + key + '\".')
            api = ApiClient()
            data = {"contents": "" + new_content}
            response = api.rest(self.url, data, 'POST')
            self.refresh()
            return response
        else:
            Utils.info('Key \"' + key + '\" already exists.')
            return "{}"

    def add_line(self, text, line=-1):
        """Add line to environment's userdata.

        Args:
            text (str): line of text to be added. (Required)
            line (int): line number to add to. If too large, default to last.

        Returns:
            str: The response from Skytap.
        """
        try:
            line = int(line)
        except ValueError:
            return "{}"  # Not an integer

        lines = self.contents.split("\n")

        new_content = ""

        line_found = False
        count = 0
        for i in lines:
            if i != "":
                if line == count:
                    new_content += (text.strip() + "\n")

                    new_content += (i.strip() + "\n")

                    line_found = True
                else:
                    new_content += (i.strip() + "\n")

            count += 1

        if not line_found:
            new_content += (text.strip() + "\n")

        Utils.info('Adding line: \"' + text + '\"')
        api = ApiClient()
        data = {"contents": new_content}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def delete_line(self, line):
        """Delete line from environment's userdata.

        Args:
            line (int): line number to delete.

        Returns:
            str: The response from Skytap.
        """
        line = str(line)

        lines = self.contents.split("\n")

        new_content = ""

        for i in lines:
            if i != "":
                if i.strip() != line.strip():
                    new_content += (i.strip() + "\n")

        Utils.info('Removing line: \"' + str(line) + '\"')
        api = ApiClient()
        data = {"contents": new_content.lstrip()}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def get_line(self, line):
        """Return content of line from environment's userdata.

        Args:
            line (int): line number to get.

        Returns:
            str: The content of the line, or "".
        """
        try:
            line = int(line)
        except ValueError:
            raise ValueError("Line must be an integer.")

        lines = self.contents.split("\n")
        return lines[line]

    def _get_values(self, contents):
        """Check userdata and set variables based on keys/values within."""
        lines = contents.split("\n")

        values = {}

        for i in lines:
            tokens = i.split()

            if len(tokens) < 2:
                continue

            # Check for valid YAML formatting in first and second tokens in
            # each line, then add those values to dict.
            if (tokens[0].endswith(":") and "#" not in tokens[0] and
                    len(tokens) > 1 and "#" not in tokens[1]):
                # If variable is a number, make it integer
                try:
                    values[tokens[0][:-1]] = int(tokens[1])
                except ValueError:
                    values[tokens[0][:-1]] = tokens[1]
                self.data[tokens[0][:-1]] = values[tokens[0][:-1]]

        return values

    def _calculate_custom_data(self):
        """Add custom data.

        Check contents and if there's something there, try to parse it, then
        add all those key/value pairs to the data block. See _get_values()
        """
        if self.contents:
            self._get_values(self.contents)
        else:
            self.data["contents"] = ""
