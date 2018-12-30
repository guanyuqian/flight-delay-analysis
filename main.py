import pandas as pd
import sys
import getopt


# 航班的平均延误时间排序，按照城市排序
# 输出:   average_flight_delay_departure.xls    作为出发地点的延迟时间
#         average_flight_delay_landing.xls      作为到达地点的延迟时间
#         average_flight_delay.xls              平均延迟时间
# city	departure_mean	    departure_sum	  departure_count
# 城市  出发平均延迟时间    总的延迟时间       出发的航班数
# landing_mean	        landing_sum	    landing_count	meam_sum
# 到达平均延迟时间     总的延迟时间   到达的航班数量     总的延迟时间平均值=出发+到达/2
# 分析：
# 输出按照总的延迟时间平均值排序，由大到小

def average_flight_delay(df):
    delay = df.groupby('departure_city')['average_delayed'].agg(['mean', 'sum', 'count'])
    delay.rename(columns={'mean': 'departure_mean', 'sum': 'departure_sum', 'count': 'departure_count'}, inplace=True)
    delay2 = df.groupby('landing_city')['average_delayed'].agg(['mean', 'sum', 'count'])
    delay2.rename(columns={'mean': 'landing_mean', 'sum': 'landing_sum', 'count': 'landing_count'}, inplace=True)
    delay.to_excel('average_flight_delay_departure.xls')
    delay2.to_excel('average_flight_delay_landing.xls')
    delay = pd.read_excel(r'average_flight_delay_departure.xls')
    delay2 = pd.read_excel(r'average_flight_delay_landing.xls')
    delay.rename(columns={'departure_city': 'city'}, inplace=True)
    delay2.rename(columns={'landing_city': 'city'}, inplace=True)
    result = pd.merge(delay, delay2, on='city')
    result['meam_sum'] = (result['departure_mean'] + result['landing_mean']) / 2.0
    result.sort_values(by=['meam_sum'], ascending=False).to_excel(r'average_flight_delay.xls')


# 度输出在city_degree.xls 按照度的大小排序
def city_degree(df):
    no_duplicate_city_connect = df[['departure_city', 'landing_city']].drop_duplicates()
    out_degree = no_duplicate_city_connect.groupby(['departure_city'])['landing_city'].count()
    in_degree = no_duplicate_city_connect.groupby(['landing_city'])['departure_city'].count()
    in_degree.to_excel('in_degree.xls')
    out_degree.to_excel('out_degree.xls')
    in_degree = pd.read_excel(r'in_degree.xls')
    out_degree = pd.read_excel(r'out_degree.xls')
    in_degree.rename(columns={'departure_city': 'in_degree', 'landing_city': 'city'}, inplace=True)
    out_degree.rename(columns={'landing_city': 'out_degree', 'departure_city': 'city'}, inplace=True)
    result = pd.merge(in_degree, out_degree, on='city')
    result['degree'] = (in_degree['in_degree'] + out_degree['out_degree'])
    result.sort_values(by=['degree'], ascending=False).to_excel('city_degree.xls')
    pass


# 航班延误时间和度之间的关系 输出在average_flight_delay_with_degree.xls
def average_flight_delay_with_degree():
    average_flight_delay = pd.read_excel(r'average_flight_delay.xls')
    degree= pd.read_excel(r'city_degree.xls')
    result = pd.merge(average_flight_delay, degree, on='city')
    result.to_excel('average_flight_delay_with_degree.xls')

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
    # process arguments
    for arg in args:
        print('process(arg)')

    df = pd.read_excel(r'data.xls')
    average_flight_delay(df)
    city_degree(df)
    average_flight_delay_with_degree()

if __name__ == "__main__":
    main()
