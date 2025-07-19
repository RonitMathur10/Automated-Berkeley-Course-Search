import pickle
import pandas as pd

second_filter_courses = pickle.load(open("/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/second_filter_courses"
, 'rb'))
print(second_filter_courses, "\n\n")

print (second_filter_courses["ESPM 50AC"])

a = list(second_filter_courses.keys())
#for course in a:
    #print (course)

#dataframe = pd.DataFrame(second_filter_courses)
#dataframe.to_csv("/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/second_filter_courses_spreadsheet.csv", index=False)