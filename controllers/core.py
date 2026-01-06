class AppController:
    LOGGER=None
    MAILER=None
    connection=None
    factory=None



    @classmethod
    def set_logger(cls,logger):
        cls.LOGGER=logger

    @classmethod
    def set_mailer(cls,mailer):
        cls.MAILER=mailer


    @classmethod
    def send_email(cls, subject, body, receivers, attachments=None, inline_attachments=None):
        if cls.MAILER is None:
            raise ValueError("MAILER is not configured. Call AppController.set_mailer() first.")

        return cls.MAILER.send_email(
            subject=subject,
            body=body,
            receivers=receivers,
            attachments=attachments,
            inline_attachments=inline_attachments
        )

    @classmethod
    def set_connection(cls, connection=None, factory=None):
        cls.connection = connection
        cls.factory = factory
        pass