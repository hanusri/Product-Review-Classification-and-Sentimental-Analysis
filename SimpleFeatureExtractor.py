def extractFeatures(data_file, flag=False):
    featureSets = []
    prodLabels = []
    sentiLabels = []

    with open(data_file, 'r') as reviews:
        for review in reviews:
            featureSet = {}
            prodLabel = ""
            sentiLabel = ""
            reviewTag = review.split("__")

            if (len(reviewTag) > 1):
                reviewSplit = reviewTag[0].lower().split("_")
                prodLabel = reviewSplit[0]
                sentiLabel = reviewSplit[1]
                review = reviewTag[1]
            if flag:
                print review

            for word in review.split():
                if word not in featureSet:
                    featureSet[word] = 1
            if flag:
                print featureSet

            featureSets += [featureSet]
            prodLabels += [prodLabel]
            sentiLabels += [sentiLabel]

    return (featureSets, prodLabels, sentiLabels)
