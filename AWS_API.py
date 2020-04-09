import boto3

def is_match(visitor_photo,permitted_photo):
    client=boto3.client('rekognition')
    response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': visitor_photo},
                                  TargetImage={'Bytes': permitted_photo})
    return len(response['FaceMatches'])>=1