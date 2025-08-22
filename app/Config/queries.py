# Leetcode GraphQL Query
lc_query = """
        query getFullUserProfile($username: String!) {
            matchedUser(username: $username) {
            username
            profile {
                realName
                aboutMe
                school
                websites
                countryName
                company
                jobTitle
                skillTags
                ranking
                userAvatar
                reputation
                solutionCount
            }
            submitStatsGlobal {
                acSubmissionNum {
                difficulty
                count
                }
            }
            badges {
                name
                icon
                hoverText
            }
            languageProblemCount {
                languageName
                problemsSolved
            }
            tagProblemCounts {
                advanced {
                tagName
                problemsSolved
                }
                intermediate {
                tagName
                problemsSolved
                }
                fundamental {
                tagName
                problemsSolved
                }
            }
            }

            userContestRanking(username: $username) {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
                badge {
                name
                }
            }
            userContestRankingHistory(username: $username) {
                attended
                trendDirection
                problemsSolved
                totalProblems
                finishTimeInSeconds
                rating
                ranking
                contest {
                title
                startTime
                }
            }
        }
        """



# GitHub GraphQL Query