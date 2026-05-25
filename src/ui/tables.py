def filter_by_category(df, category):
    return df if category == 'all' else df[df['category']==category]
