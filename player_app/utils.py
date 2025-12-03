from datetime import date

def get_season_cutoff(today: date | None = None) -> date:
    """
    Return 1 September of the *current* season:
    - If today >= 1 Sep current year => cutoff = 1 Sep current year
    - Else => cutoff = 1 Sep previous year
    """
    if today is None:
        today = date.today()
    sept1_this_year = date(today.year, 9, 1)
    if today >= sept1_this_year:
        return sept1_this_year          # e.g. 2025-09-01 for Dec 2025
    else:
        return date(today.year - 1, 9, 1)

def age_on_date(dob: date, target: date) -> int:
    years = target.year - dob.year
    if (target.month, target.day) < (dob.month, dob.day):
        years -= 1
    return years

def age_for_current_season(dob: date) -> int:
    cutoff = get_season_cutoff()
    return age_on_date(dob, cutoff)
