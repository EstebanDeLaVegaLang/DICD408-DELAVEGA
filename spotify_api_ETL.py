class SpotifyAPI:
    """A class for interacting with the Spotify API."""

    # ...

    def get_user_data(self):
        """Get user data for the specified user ID."""
        return self._authenticated_request(f"{self.USER_ENDPOINT}/{self.user_id}")

    def get_playlists(self):
        """Get playlists for the specified user ID."""
        return self._authenticated_request(f"{self.USER_ENDPOINT}/{self.user_id}/{self.PLAYLISTS_ENDPOINT}")["items"]
    
    