import boto3

def compare_faces(sourceFile, targetFile):
    # input path of source and target images
    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')
    # print('finished reading images')

    response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    # print(response)
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with confidence of ' + similarity + '%')

    imageSource.close()
    imageTarget.close()     
    return len(response['FaceMatches'])          

def main():
    # change image path before you run
    source_file="img1.jpg"
    target_file="img2.jpg"
    face_matches=compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))


if __name__ == "__main__":
    main()