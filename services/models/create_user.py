from models.user import User

def create_user(session, **user_data):
    new_user = User(
        **user_data
        # addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    # sandy = User(
    #     name="sandy",
    #     fullname="Sandy Cheeks",
    #     addresses=[
    #         Address(email_address="sandy@sqlalchemy.org"),
    #         Address(email_address="sandy@squirrelpower.org"),
    #     ],
    # )
    # patrick = User(name="patrick", fullname="Patrick Star")

    session.add(new_user)

    return new_user
