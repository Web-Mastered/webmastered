from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_userinfo_claims(self, request):
        claims = super().get_userinfo_claims(request)
        claims["name"] = str(request.user.first_name) + " " + str(request.user.last_name)
        claims["email"] = str(request.user.email)
        return claims