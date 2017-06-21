# Jobs.pymi.vn Crawlers

[![CircleCI](https://circleci.com/gh/pymivn/pyjobs_crawlers.svg?style=svg)](https://circleci.com/gh/pymivn/pyjobs_crawlers)

Run all spiders by

```
./runner
```

Or run single spider

```
./runner CareerBuilder
```

# Test / lint

Để test style/lint chạy:

```
make lint
```

Chú ý, máy bạn cần cài sẵn `make`.

Để test các spider, chạy:

```
make test
```

# Đóng góp

- Tìm hiểu về [Scrapy](https://scrapy.org/)
- Fork project về tài khoản GitHub của bạn: https://github.com/pymivn/pyjobs_crawlers#fork-destination-box (bấm nút Fork góc trên bên phải).
- Chỉnh sửa các spiders trong spiders/ hoặc thêm spider mới
- Commit, push rồi tạo Pull Request https://github.com/pymivn/pyjobs_crawlers/compare

# Các tiêu chí về spider
- Mỗi job phải có tối thiểu 5 thông tin:
  ```
  ['name', 'province', 'url', 'work', 'specialize']
  ```
- Code chuẩn Pep8, độ dài mỗi dòng giới hạn là 100 ký tự.
- Python 2 (project được tạo trước khi Scrapy hỗ trợ Python3)

# TODO
- Thêm status của các crawler vào web

# Phụ lục
- Sử dụng [Splash](http://splash.readthedocs.io/en/stable/install.html) và [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) để crawl các trang web render nội dung bằng Javascript
