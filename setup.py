if __name__ == "__main__":
    from setuptools import setup, find_namespace_packages # type: ignore[import]

# from https://github.com/seanbreckenridge/HPI/blob/master/setup.py
def subpackages():
    # make sure subpackages are only in the my/ folder (not in tests or other folders here)
    for p in find_namespace_packages(".", include=("my.*",)):
        if p.startswith("my"):
            yield p

if __name__ == "__main__":
    setup(
        name=f"HPI-overlay",  # use a different name from karlicoss/HPI, for confusion regarding egg-link reasons
        use_scm_version={
            "local_scheme": "dirty-tag",
        },
        zip_safe=False,
        packages=list(subpackages()),
        url=f"https://github.com/jussihuotari/HPI-overlay",
        author="Jussi Huotari",
        author_email="jussi@example.com",
        description="A Python interface to my life",
        python_requires=">=3.8",
    )


