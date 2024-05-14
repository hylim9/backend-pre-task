-- INSERT contact
INSERT INTO contact (
    profile_picture,
    name,
    email,
    phone_number,
    company,
    job_title,
    description,
    address,
    birth_date,
    homepage_url, 
    created_at, 
    created_by, 
    updated_at, 
    updated_by
) 
VALUES (
    'https://oopy.lazyrockets.com/api/rest/cdn/image/0196375a-2c5d-4ccd-afd8-d5034cc2cbe0.png', 
    '임현영', 
    'test@gmail.com', 
    '010-1234-1234', 
    '구글', 
    '과장', 
    '', 
    null, 
    null, 
    null, 
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
 ),
 (
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnv42OT9xKWPPynLHlQPhYlIxWxxJNQBW7qbD-4AA5gQ&s', 
    'John Doe', 
    'johndoe@gmail.com', 
    '010-9999-2277', 
    '아마존', 
    '대리', 
    '테스트', 
    null, 
    null, 
    null, 
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
 ),
 (
    'https://picsum.photos/100', 
    '김루피', 
    'rr@gmail.com', 
    '010-1111-3030', 
    '뽀로로', 
    '사원', 
    '넵', 
    null, 
    null, 
    null, 
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
 ),
 (
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnv42OT9xKWPPynLHlQPhYlIxWxxJNQBW7qbD-4AA5gQ&s', 
    'Kevin', 
    'kk@gmail.com', 
    '010-9999-7777', 
    'K Corp', 
    '대표', 
    '호호호', 
    null, 
    null, 
    null, 
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
 ),
 (
    'https://picsum.photos/200', 
    '김김김', 
    'ahkima@gmail.com', 
    '010-2331-8867', 
    '킴', 
    '사원', 
    '', 
    null, 
    null, 
    null, 
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
 );

-- INSERT label
INSERT INTO label (
    name,
    created_at, 
    created_by, 
    updated_at, 
    updated_by
)
VALUES (
    '집',
    datetime('now'), 
    'admin', 
    datetime('now'),
    null
), 
(
    '직장',
    datetime('now'), 
    'admin', 
    datetime('now'),
    null

),
(
    '기타',
    datetime('now'), 
    'admin', 
    datetime('now'),
    null

);

-- INSERT contact_label;
INSERT INTO contact_label (
    contact_id,
    label_id
)
VALUES (1, 1), (1, 2), (2, 3);