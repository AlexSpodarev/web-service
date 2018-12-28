# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [0.0.4] - 2018-12-28

### Added
- Database extended from 2 to 6 columns - [@AlexSpodarev](https://github.com/AlexSpodarev)
- Added support for Precision 6262 Turbo, the code is now capable for 700whp - [@AlexSpodarev](https://github.com/AlexSpodarev)

### Removed
- Removed unused code and optimized code syntax - [@AlexSpodarev](https://github.com/AlexSpodarev)

### Changed
- Totally reconstructed GET / POST code and helper functions - [@AlexSpodarev](https://github.com/AlexSpodarev)

## [0.0.3] - 2018-12-26

### Added
- Added db_migration file to extend existing DB to one more dimension - [@AlexSpodarev](https://github.com/AlexSpodarev)

### Removed
### Changed

## [0.0.2] - 2018-12-25

### Added
- CHANGELOG.md file to keep track of changes - [@tommybrecher](https://github.com/tommybrecher)
- requirments.txt so users who clone the repository can run `pip install -r requriments.txt` - [@tommybrecher](https://github.com/tommybrecher) 
- Comments on chunks of the code where the logic gets complex - [@tommybrecher](https://github.com/tommybrecher)
- A method which aborts invalid requests with a 404 unless a specific code is provided `reject_invalid_request()` - [@tommybrecher](https://github.com/tommybrecher)
- logging statements everywhere for easier debugging (shouldn't run anyways if when calling app.run() we don't set it to debugging - [@tommybrecher](https://github.com/tommybrecher)

### Removed
- Commented out code 

### Changed
- The logic of checking if data is in the database by using a separate, generic function - [@tommybrecher](https://github.com/tommybrecher)
- The logic of appending content to the database by using a separate, generic function - [@tommybrecher](https://github.com/tommybrecher)
- The default IP address we are listening on - [@tommybrecher](https://github.com/tommybrecher)

## [0.0.1] - 2018-12-24

### Added
- Create the repository and upload the code - [@AlexSpodarev](https://github.com/AlexSpodarev)
- Added @tommybrecher as a contributer - [@AlexSpodarev](https://github.com/AlexSpodarev)

### Removed

### Changed
