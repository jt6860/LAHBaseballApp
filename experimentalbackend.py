# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:10:54 2025

@author: Owner
"""
import pandas as pd
import numpy as np
from flask import Flask, jsonify, make_response
from flask_cors import CORS

# Age
def calculate_age_with_missing_check(df, birth_year_col, year_id_col, age_col):

    def calculate_row_age(row):
        birth_year = row[birth_year_col]
        year_id = row[year_id_col]

        if birth_year == 'missing':
            return "birthYear missing"
        elif year_id == 'missing':
            return "yearID missing"
        else:
            try:
                return int(year_id) - int(birth_year)
            except ValueError:
                return "Invalid data"

    df[age_col] = df.apply(calculate_row_age, axis=1)
    return df

# AVG
def calculate_avg_with_missing_check(df, hits_col, ab_col, battingAverage_col):

    def calculate_row_avg(row):
        hits = row[hits_col]
        atbats = row[ab_col]

        if atbats == 0:
            return "No At-Bats"
        else:
            try:
                return round((hits / atbats), 3)
            except ValueError:
                return "Invalid data"

    df[battingAverage_col] = df.apply(calculate_row_avg, axis=1)
    return df

# SLG
def calculate_slg_with_missing_check(df, hits_col, doubles_col, triples_col, hr_col, ab_col, sluggingPct_col):

    def calculate_row_slg(row):
        hits = row[hits_col]
        doubles = row[doubles_col]
        triples = row[triples_col]
        hrs = row[hr_col]
        atbats = row[ab_col]

        if atbats == 0:
            return "No At-Bats"
        else:
            try:
                return round((hits + (doubles * 2) + (triples * 3) + (hrs * 4)) / atbats, 3)
            except ValueError:
                return "Invalid data"

    df[sluggingPct_col] = df.apply(calculate_row_slg, axis=1)
    return df

# OBP
def calculate_obp_with_missing_check(df, hits_col, walks_col, hbp_col, sf_col, ab_col, onBasePct_col):

    def calculate_row_obp(row):
        hits = row[hits_col]
        walks = row[walks_col]
        hbp = row[hbp_col]
        sfs = row[sf_col]
        atbats = row[ab_col]

        if atbats == 0:
            return "No At-Bats"
        else:
            try:
                return round((hits + walks + hbp) / (atbats + walks + hbp + sfs), 3)
            except ValueError:
                return "Invalid data"

    df[onBasePct_col] = df.apply(calculate_row_obp, axis=1)
    return df

# OPS
def calculate_ops_with_missing_check(df, onBasePct_col, sluggingPct_col, ops_col):

    def calculate_row_ops(row):
        obp = row[onBasePct_col]
        slg = row[sluggingPct_col]
        
        if obp == "No At-Bats":
            return "No At-Bats"
        else:
            try:
                return round(obp + slg, 3)
            except ValueError:
                return "Invalid data"

    df[ops_col] = df.apply(calculate_row_ops, axis=1)
    return df


# Read in CSVs
batting_df = pd.read_csv("Batting.csv", encoding="utf-8", encoding_errors="replace")
pitching_df = pd.read_csv("Pitching.csv", encoding="utf-8", encoding_errors="replace")

# Create Name column using nameFirst and nameLast
people_df = pd.read_csv("People.csv", encoding="utf-8", encoding_errors="replace")
people_df['name'] = people_df['nameFirst'] + ' ' + people_df['nameLast']

# Batting/People merge
batting_data = pd.merge(batting_df, people_df, on='playerID', how='inner')
batting_data = batting_data.drop(columns=["stint", "lgID", "ID", "G_batting", "G_old", "deathYear", "deathMonth", "deathDay", "deathCountry", "deathState", "deathCity", "CS", "nameGiven", "nameFirst", "nameLast", "birthCity", "birthCountry", "birthState", "debut", "bbrefID", "retroID", "finalGame", "birthMonth", "birthDay" ])

# Pitching/People merge
pitching_data = pd.merge(pitching_df, people_df, on='playerID', how='inner')
pitching_data = pitching_data.drop(columns=["stint", "lgID", "ID", "bats", "deathYear", "deathMonth", "deathDay", "deathCountry", "deathState", "deathCity", "nameGiven", "nameFirst", "nameLast", "birthCity", "birthCountry", "birthState", "debut", "bbrefID", "retroID", "finalGame", "birthMonth", "birthDay" ])

# Convert Batter Height from inches to feet.inches
batting_data['height'] = batting_data['height'] / 12
batting_data['height'] = np.ceil(batting_data['height'] * 10) / 10

# Convert Pitchter Height from inches to feet.inches
pitching_data['height'] = pitching_data['height'] / 12
pitching_data['height'] = np.ceil(pitching_data['height'] * 10) / 10

# Create Filtered dataframe based on if Batter had more than 0 at-bats in a season.
batting_data = batting_data[batting_data['AB'] > 0]

# Create Filtered dataframe based on if Pitcher got more than 0 outs pitched in a season.
pitching_data = pitching_data[pitching_data['IPouts'] > 0]

# Fill batting NaN values with 0
batting_data['RBI'] = batting_data['RBI'].fillna(0)
batting_data['SB'] = batting_data['SB'].fillna(0)
batting_data['SO'] = batting_data['SO'].fillna(0)
batting_data['IBB'] = batting_data['IBB'].fillna(0)
batting_data['HBP'] = batting_data['HBP'].fillna(0)
batting_data['SH'] = batting_data['SH'].fillna(0)
batting_data['SF'] = batting_data['SF'].fillna(0)
batting_data['GIDP'] = batting_data['GIDP'].fillna(0)

# Fill remaining NaN values with missing, fill all pitching stat NaN values with missing instead of 0 to avoid skew.
print(pitching_data.isna().sum())
filled_batting_data = batting_data.fillna('missing')
filled_pitching_data = pitching_data.fillna('missing')


# Calculate Age, Drop Birth Year
clean_batting_data = calculate_age_with_missing_check(filled_batting_data, 'birthYear', 'yearID', 'age')
clean_batting_data = clean_batting_data.drop(columns=["birthYear"])
clean_pitching_data = calculate_age_with_missing_check(filled_pitching_data, 'birthYear', 'yearID', 'age')
clean_pitching_data = clean_pitching_data.drop(columns=["birthYear"])

# Calculate Batting Average
clean_batting_data = calculate_avg_with_missing_check(clean_batting_data, 'H', 'AB', 'battingAvg')

# Calculate On-Base Percentage and Slugging Percentage
clean_batting_data = calculate_slg_with_missing_check(clean_batting_data, 'H', '2B', '3B', 'HR', 'AB', 'sluggingPct')
clean_batting_data = calculate_obp_with_missing_check(clean_batting_data, 'H', 'BB', 'HBP', 'SF', 'AB', 'onBasePct')

# Calculate OPS (OnBase Plus Slug)
clean_batting_data = calculate_ops_with_missing_check(clean_batting_data, 'onBasePct', 'sluggingPct', 'OPS')

# Reorder Columns
bat_col_order = ["name", "playerID", "age", "yearID", "teamID", "height", "weight", "bats", "throws", "OPS", "battingAvg", "sluggingPct", "onBasePct", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "SB", "BB", "SO", "IBB", "HBP", "SH", "SF", "GIDP"]
pitch_col_order = ["name", "playerID", "age", "yearID", "teamID", "height", "weight", "throws", "W", "L", "SV", "ERA", "ER", "SO", "G", "GS", "CG", "SHO", "IPouts", "H", "HR", "BB", "BAOpp", "WP", "IBB", "HBP", "BK", "BFP", "GF", "R", "SH", "SF", "GIDP"]
clean_batting_data = clean_batting_data[bat_col_order]
clean_pitching_data = clean_pitching_data[pitch_col_order]


# App execution functionality and route definitions
app = Flask(__name__)

CORS(app)

@app.route('/api/bat_stats/<int:season>')
def get_bat_stats(season):
    try:
        imported_batstats = clean_batting_data[clean_batting_data['yearID'] == season]
   
        # Check if the DataFrame is empty
        if imported_batstats.empty:
            return jsonify({'error': f'No batting statistics found for season {season}'}), 404

        ingested_batstats = [
            {
                'name': player['name'],
                'season': season,
                'Age': player['age'],
                'Team': player['teamID'],
                'Height': player['height'],
                'Weight': player['weight'],
                'Bats': player['bats'],
                'Throws': player['throws'],
                'OPS': player['OPS'],
                'SLG': player['sluggingPct'],
                'OBP': player['onBasePct'],
                'AVG': player['battingAvg'],
                'AB': player['AB'],
                'H': player['H'],
                'doubles': player['2B'],
                'triples': player['3B'],
                'HR': player['HR'],
                'R': player['R'],
                'RBI': player['RBI'],
                'SB': player['SB'],
                'SO': player['SO'],
                'IBB': player['IBB'],
                'HBP': player['HBP'],
                'SF': player['SF'],
                'SH': player['SH'],
                'GIDP': player['GIDP']
            }
            for player in imported_batstats.to_dict('records')
        ]
                         
        response = make_response(jsonify(ingested_batstats))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        return jsonify({'error': f'Error processing batting data: {str(e)}'}), 500


@app.route('/api/pitch_stats/<int:season>')
def get_pitch_stats(season):
    try:
        imported_pitchstats = clean_pitching_data[clean_pitching_data['yearID'] == season]
   
        # Check if the DataFrame is empty
        if imported_pitchstats.empty:
            return jsonify({'error': f'No pitching statistics found for season {season}'}), 404

#["name", "playerID", "age", "yearID", "teamID", "height", "weight", "throws", "W", "L", "SV", "ERA", "ER", "SO", "G", "GS", "CG", "SHO", "IPouts", "H", "HR", 
#"BB", "BAOpp", "WP", "IBB", "HBP", "BK", "BFP", "GF", "R", "SH", "SF", "GIDP"]
        ingested_pitchstats = [
            {
                'name': player['name'],
                'season': season,
                'Age': player['age'],
                'Team': player['teamID'],
                'Height': player['height'],
                'Weight': player['weight'],
                'Throws': player['throws'],
                'W': player['W'],
                'L': player['L'],
                'SV': player['SV'],
                'ERA': player['ERA'],
                'ER': player['ER'],
                'SO': player['SO'],
                'G': player['G'],
                'GS': player['GS'],
                'CG': player['CG'],
                'SHO': player['SHO'],
                'IPouts': player['IPouts'],
                'H': player['H'],
                'HR': player['HR'],
                'BB': player['BB'],
                'BAOpp': player['BAOpp'],
                'WP': player['WP'],
                'IBB': player['IBB'],
                'HBP': player['HBP'],
                'BK': player['BK'],
                'BFP': player['BFP'],
                'GF': player['GF'],
                'R': player['R'],
                'SH': player['SH'],
                'SF': player['SF'],
                'GIDP': player['GIDP']
            }
            for player in imported_pitchstats.to_dict('records')
        ]
        
        response = make_response(jsonify(ingested_pitchstats))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        return jsonify({'error': f'Error processing Pitching data: {str(e)}'}), 500

    
if __name__ == '__main__':
    app.run(debug=True)