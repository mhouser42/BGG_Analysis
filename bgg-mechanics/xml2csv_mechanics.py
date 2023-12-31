import os
import xml.etree.ElementTree as ET
import datetime
import config
import csv

def main():
    all_mechanics = []
    folder = os.path.join('.', 'data')
    start_time = datetime.datetime.now()
    all_output = []
    with open(os.path.join('.', 'all_data.csv'), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(config.max_game):
            current_time = datetime.datetime.now()
            seconds_passed = (current_time-start_time).total_seconds()
            total_seconds = config.max_game / float(i+1) * seconds_passed
            print(f'{round(i/config.max_game * 100, 2)}% done, {total_seconds-seconds_passed} seconds remain')
            filename = os.path.join(folder, f'game{i}.xml')
            if os.path.isfile(filename):
                xml_tree = ET.parse(filename)
                boardgame = xml_tree.find('boardgame')
                error = boardgame.find('error')
                if error is not None:
                    continue
                statistics = boardgame.find('statistics')
                ratings = statistics.find('ratings')
                average = ratings.find('average')
                game_rating = float(average.text)
                bayesaverage = ratings.find('bayesaverage')
                bayes_rating = float(bayesaverage.text)
                if bayes_rating==0:
                    continue
                mechanics = boardgame.findall('boardgamemechanic')
                mechanics_values = []
                for mechanic in all_mechanics:
                    mechanics_values.append(0)
                for mechanic in mechanics:
                    if mechanic.text not in all_mechanics:
                        all_mechanics.append(mechanic.text)
                        mechanics_values.append(1)
                    else:
                        mechanics_values[all_mechanics.index(mechanic.text)] = 1
                output = []
                output.append(game_rating)
                output.append(bayes_rating)
                for element in mechanics_values:
                    output.append(element)
                all_output.append(output)
        header_output = ['rating', 'bayes_rating']
        for element in all_mechanics:
            header_output.append(element)
        csv_writer.writerow(header_output)
        for element in all_output:
            while len(element)<len(all_mechanics)+2:
                element.append(0)
            csv_writer.writerow(element)

if __name__ == '__main__':
    main()
