class Convert:
    class Date:
        @classmethod
        def raw_date(cls, date, sep='.'):
            day = str(date.day)
            if len(day) == 1:
                day = '0' + day
            month = str(date.month)
            if len(month) == 1:
                month = '0' + month
            year = str(date.year)[-2:]
            return f'{day}{sep}{month}{sep}{year}'

        @classmethod
        def raw_time(cls, date, sep=':'):
            hours = str(date.hour)
            if len(hours) == 1:
                hours = '0' + hours
            minutes = str(date.minute)
            if len(minutes) == 1:
                minutes = '0' + minutes
            seconds = str(date.second)
            if len(seconds) == 1:
                seconds = '0' + seconds
            return f'{hours}{sep}{minutes}{sep}{seconds}'

        @classmethod
        def raw_datetime(cls, date, date_sep='.', time_sep=':'):
            result_date = cls.raw_date(date, date_sep)
            result_time = cls.raw_time(date, time_sep)
            return f'{result_date} {result_time}'
