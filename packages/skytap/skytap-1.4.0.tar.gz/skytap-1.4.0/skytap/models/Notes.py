"""Support for notes that are attached to VMs and environments."""
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.Note import Note
from skytap.models.SkytapGroup import SkytapGroup


class Notes(SkytapGroup):
    """A collection of notes."""

    def __init__(self, note_json, env_url):
        """Build note list."""
        super(Notes, self).__init__()
        self.load_list_from_json(note_json, Note)
        self.url = env_url + '/notes.json'

    def add(self, note):
        """Add one note.

        Args:
            note (str): The note text to add.

        Returns:
            str: The response from Skytap, typically the new note.
        """
        Utils.info('Adding note: ' + note)
        api = ApiClient()
        data = {"text": note}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def delete(self, note):
        """Delete one note.

        Args:
            note: The :class:`~skytap.models.Note` to delete.

        Returns:
            str: The response from Skytap.

        Raises:
            TypeError: If note is not a Note object.
        """
        if note is None:
            return False
        if not isinstance(note, Note):
            raise TypeError
        Utils.info('Deleting note ID: ' + str(note.id))
        api = ApiClient()
        url = self.url.replace('.json', '/' + str(note.id))
        response = api.rest(url,
                            {},
                            'DELETE')
        self.refresh()
        return response

    def oldest(self):
        """Return the oldest note.

        Returns:
            ~skytap.models.Note: The oldest note.

        Used most often to delete the oldest note.

        Example:

        .. code-block:: python

            notes = skytap.Environtments().first.notes
            print(notes.oldest().text)
            # notes.delete(notes.oldest())  # most common use case.
        """
        target = None
        for each_note in self.data:
            if target is None:
                target = self.data[each_note]
                continue
            if self.data[each_note].updated_at > target.updated_at:
                target = self.data[each_note]
        return target

    def newest(self):
        """Return the newest note.

        Returns:
            ~skytap.models.Note: The newest note.
        """
        target = None
        for each_note in self.data:
            if target is None:
                target = self.data[each_note]
                continue
            if self.data[each_note].updated_at < target.updated_at:
                target = self.data[each_note]
        return target

    def delete_all(self):
        """Delete all notes.

        Returns:
            int: count of deleted notes.

        Use with care!
        """
        Utils.debug('Deleting all notes.')
        keys = self.data.keys()
        count = len(keys)
        for key in keys:
            self.delete(self.data[key])
        self.refresh()
        return count

    def refresh(self):
        """Refresh the notes.

        Raises:
            KeyError: if the Notes object doesn't
                have a url attribute for some reason.

        Go back to Skytap and get the notes again. Useful when you've changed
        the notes and to make sure you're current.
        """
        if len(self.url) == 0:
            return KeyError
        api = ApiClient()
        note_json = api.rest(self.url)
        self.load_list_from_json(note_json, Note)
