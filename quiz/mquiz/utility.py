def add_solvers(title, solvers):  # list of solvers
    qzs = quizes.find_one({'_id': title})
    l = qzs.get('solvers')
    if l:
        l.extend(solvers)
        l = list(set(l))
    else:
        l = list(set(solvers))
    quizes.update_one({'_id': title}, {'$set': {'solvers': l}})
