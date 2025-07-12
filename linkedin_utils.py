
def build_linkedin_jobs_url(company_id: int, geo_id: int = 101620260) -> str:
    """
    Construct LinkedIn job search URL for a company using its internal ID.

    Args:
        company_id (int): LinkedIn internal company ID.
        geo_id (int): LinkedIn geoId for location (default is Israel: 101620260)

    Returns:
        str: Constructed LinkedIn jobs URL.
    """
    return (
        f"https://www.linkedin.com/jobs/search/?f_C={company_id}&geoId={geo_id}"
    )
