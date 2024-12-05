from datetime import datetime

def reformat_date(date_str: str, airline: str) -> str:
    """
    Reformat a date based on the airline's expected format.

    Args:
        date_str (str): The input date in 'YYYY-MM-DD' format.
        airline (str): The airline name ("airpeace", "greenafrica", "arikair", "ibomair").

    Returns:
        str: Reformatted date string.
    """
    try:
        # Parse the input date (expecting 'YYYY-MM-DD' format)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        if airline.lower() in ["airpeace", "arikair", "ibomair"]:
            # These airlines require 'dd.mm.yyyy' format
            return date_obj.strftime('%d.%m.%Y')
        elif airline.lower() == "greenafrica":
            # GreenAfrica requires 'yyyy-mm-dd' format
            return date_obj.strftime('%Y-%m-%d')
        else:
            raise ValueError(f"Unknown airline: {airline}")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected 'YYYY-MM-DD'.")
