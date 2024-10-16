from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the CSV file into a DataFrame
csv_file = os.path.join(current_dir, 'testOverBookingProbability.csv')
df = pd.read_csv(csv_file)

@app.route('/<int:collection_id>', methods=['GET'])
def get_exceedance_probability(collection_id):
    try:
        row = df[df['collection_id'] == collection_id]
        if row.empty:
            return jsonify({
                'error': 'collection_id not found',
                'message': f'No data found for collection_id {collection_id}'
            }), 404
        
        exceedance_prob_request = row['exceedance_probability_cpu_request'].values[0]
        
        return jsonify({
            'collection_id': collection_id,
            'exceedance_probability_cpu_request': exceedance_prob_request
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing the request.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6186)

